import multiprocessing
from multiprocessing import Process
import time
import copy
import logging
import re
import os
import sys
import gc
import socket

from cloudscheduler.lib.attribute_mapper import map_attributes
from cloudscheduler.lib.db_config import Config
from cloudscheduler.lib.ProcessMonitor import ProcessMonitor
from cloudscheduler.lib.poller_functions import \
    delete_obsolete_database_items, \
    get_inventory_item_hash_from_database, \
    test_and_set_inventory_item_hash, \
    build_inventory_for_condor, \
    start_cycle, \
    wait_cycle

import htcondor
import classad
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


# condor likes to return extra keys not defined in the projection
# this function will trim the extra ones so that we can use kwargs
# to initiate a valid table row based on the data returned
def trim_keys(dict_to_trim, key_list):
    keys_to_trim = ["Owner"]
    for key in dict_to_trim:
        if key == "group_name":
            continue
        if key not in key_list or isinstance(dict_to_trim[key], classad._classad.Value):
            keys_to_trim.append(key)
    for key in keys_to_trim:
        dict_to_trim.pop(key, None)
    return dict_to_trim

def job_poller():
    multiprocessing.current_process().name = "Job Poller"
    job_attributes = ["TargetClouds", "JobStatus", "RequestMemory", "GlobalJobId", "HoldReason",
                      "RequestDisk", "RequestCpus", "RequestScratch", "RequestSwap", "Requirements",
                      "JobPrio", "ClusterId", "ProcId", "User", "VMInstanceType", "VMNetwork",
                      "VMImage", "VMKeepAlive", "VMMaximumPrice", "VMUserData", "VMJobPerCore", "Owner",
                      "EnteredCurrentStatus", "QDate", "HoldReasonCode", "HoldReasonSubCode", "LastRemoteHost" ]
    # Not in the list that seem to be always returned:
    # FileSystemDomian, MyType, ServerTime, TargetType
    cycle_start_time = 0
    new_poll_time = 0
    poll_time_history = [0,0,0,0]
    fail_count = 0
    inventory = {}
    delete_cycle = True
    cycle_count = 0
    condor_inventory_built = False
    uncommitted_updates = 0

    config = Config('/etc/cloudscheduler/cloudscheduler.yaml', os.path.basename(sys.argv[0]), pool_size=4)


    JOB = config.db_map.classes.condor_jobs
    CLOUDS = config.db_map.classes.csv2_clouds
    GROUPS = config.db_map.classes.csv2_groups
    USERS = config.db_map.classes.csv2_user_groups

    try:
        inventory = get_inventory_item_hash_from_database(config.db_engine, JOB, 'global_job_id', debug_hash=(config.log_level<20))
        while True:
            #
            # Setup - initialize condor and database objects and build user-group list
            #
            new_poll_time, cycle_start_time = start_cycle(new_poll_time, cycle_start_time)
            config.db_open()
            db_session = config.db_session
            groups = db_session.query(GROUPS)
            condor_hosts_set = set() # use a set here so we dont re-query same host if multiple groups have same host
            condor_host_groups = {}
            group_users = {}
            for group in groups:
                if group.htcondor_container_hostname is not None and group.htcondor_container_hostname != "":
                    condor_central_manager = group.htcondor_container_hostname
                    condor_hosts_set.add(group.htcondor_container_hostname)
                elif group.htcondor_fqdn is not None and group.htcondor_fqdn != "":
                    condor_central_manager = group.htcondor_fqdn
                    condor_hosts_set.add(group.htcondor_fqdn)   
                else:
                    # no condor location set
                    continue                

                if condor_central_manager not in condor_host_groups:
                    condor_host_groups[condor_central_manager] = [group.group_name]
                else:
                    condor_host_groups[condor_central_manager].append(group.group_name)

                # build group_users dict
                users = config.db_session.query(USERS).filter(USERS.group_name == group.group_name)
                htcondor_other_submitters = group.htcondor_other_submitters
                if htcondor_other_submitters is not None:
                    user_list = group.htcondor_other_submitters.split(',')
                else:
                    user_list = []
                # need to append users from group defaultts (htcondor_supplementary_submitters) here
                # alternatively we can just have 2 lists and check both wich would save on memory if there was a ton of users but cost cycles
                for usr in users:
                    user_list.append(usr.username)

                group_users[group.group_name] = user_list

            uncommitted_updates = 0
            forgein_jobs = 0
            for condor_host in condor_hosts_set:
                forgein_jobs = 0
                logging.info("Polling condor host: %s" % condor_host)
                try:
                    coll = htcondor.Collector(condor_host)
                    scheddAd = coll.locate(htcondor.DaemonTypes.Schedd, condor_host)
                    condor_session = htcondor.Schedd(scheddAd)

                except Exception as exc:
                    logging.error("Failed to locate condor daemon, skipping: %s" % condor_host)
                    logging.debug(exc)
                    continue


                if not condor_inventory_built:
                    build_inventory_for_condor(inventory, db_session, CLOUDS)
                    condor_inventory_built = True

                # Retrieve jobs.
                
                logging.debug("getting job list from condor")
                try:
                    job_list = condor_session.xquery(
                        projection=job_attributes
                        )
                except Exception as exc:
                    logging.error("Failed to get jobs from condor scheddd object, aborting poll on host: %s" % condor_host)
                    logging.error(exc)
                    continue

                # Process job data & insert/update jobs in Database
                abort_cycle = False
                job_errors = {}
                for job_ad in job_list:
                    job_dict = dict(job_ad)
                    if "Requirements" in job_dict:
                        job_dict['Requirements'] = str(job_dict['Requirements'])
                        # Parse group_name out of requirements
                        try:
                            pattern = '(group_name is ")(.*?)(")'
                            grp_name = re.search(pattern, job_dict['Requirements'])
                            job_dict['group_name'] = grp_name.group(2)
                        except Exception as exc:
                            logging.debug("No group name found in requirements expression... ignoring foreign job.")
                            forgein_jobs = forgein_jobs+1
                            if "nogrp" not in job_errors:
                                job_errors["nogrp"] = 1
                            else:
                                job_errors["nogrp"] = job_errors["nogrp"] + 1
                            continue
                    else:
                        logging.debug("No requirements attribute found, not a csv2 job... ignoring foreign job.")
                        forgein_jobs = forgein_jobs+1
                        if "noreq" not in job_errors:
                            job_errors["noreq"] = 1
                        else:
                            job_errors["noreq"] = job_errors["noreq"] + 1
                        continue

                    #check group_name is valid for this host
                    if job_dict['group_name'] not in condor_host_groups[condor_host]:
                        # not a valid group for this host
                        logging.debug("%s is not a valid group for %s, ignoring foreign job." % (job_dict['group_name'], condor_host))
                        forgein_jobs = forgein_jobs+1
                        if "invalidgrp" not in job_errors:
                            job_errors["invalidgrp"] = 1
                        else:
                            job_errors["invalidgrp"] = job_errors["invalidgrp"] + 1

                        continue

                    # check if user is valid for this group
                    if job_dict['Owner'] not in group_users[job_dict['group_name']]:
                        # this user isn''t registered with this group and thus cannot submit jobs to it
                        logging.debug("User '%s' is not registered to submit jobs to %s, excluding as foreign job." % (job_dict['Owner'], job_dict['group_name']))
                        forgein_jobs = forgein_jobs+1
                        if "invalidusr" not in job_errors:
                            job_errors["invalidusr"] = 1
                        else:
                            job_errors["invalidusr"] = job_errors["invalidgrp"] + 1
                        continue

                    # Some jobs have an expression for the request disk causing us to store a string
                    # this should resolve the expression or us an alternative if unable
                    try:
                        job_dict["RequestDisk"] = int(job_dict["RequestDisk"])
                    except Exception as exc:
                        job_dict["RequestDisk"] = int(job_dict["DiskUsage"])

                    job_dict = trim_keys(job_dict, job_attributes)
                    job_dict, unmapped = map_attributes(src="condor", dest="csv2", attr_dict=job_dict)
                    logging.debug(job_dict)
                    if unmapped:
                        logging.error("attribute mapper found unmapped variables:")
                        logging.error(unmapped)

                    # Check if this item has changed relative to the local cache, skip it if it's unchanged
                    if test_and_set_inventory_item_hash(inventory, job_dict["group_name"], "-", job_dict["global_job_id"], job_dict, new_poll_time, debug_hash=(config.log_level<20)):
                        continue

                    logging.debug("Adding job %s", job_dict["global_job_id"])
                    new_job = JOB(**job_dict)
                    try:
                        db_session.merge(new_job)
                        uncommitted_updates += 1
                    except Exception as exc:
                        logging.error("Failed to merge job entry, aborting cycle...")
                        logging.error(exc)
                        abort_cycle = True
                        break
                        
                if forgein_jobs > 0:
                    logging.info("Ignored %s forgein jobs" % forgein_jobs)
                    if "nogrp" in job_errors:
                        logging.info("%s ignored for missing group name" % job_errors["nogrp"])
                    if "noreq" in job_errors:
                        logging.info("%s ignored for missing requirements string" % job_errors["noreq"])
                    if "invalidgrp" in job_errors:
                        logging.info("%s ignored for submitting to invalid group for host" % job_errors["invalidgrp"])
                    if "invalidusr" in job_errors:
                        logging.info("%s ignored for submitting to a group without permission" % job_errors["invalidusr"])


                if abort_cycle:
                    del condor_session
                    config.db_close()
                    del db_session
                    break

            if uncommitted_updates > 0:
                try:
                    db_session.commit()
                    logging.info("Job updates committed: %d" % uncommitted_updates)
                except Exception as exc:
                    logging.error("Failed to commit new jobs, aborting cycle...")
                    logging.error(exc)
                    config.db_close()
                    time.sleep(config.sleep_interval_job)
                    continue

            if delete_cycle:
                # Check for deletes
                delete_obsolete_database_items('Jobs', inventory, db_session, JOB, 'global_job_id', poll_time=new_poll_time)
                delete_cycle = False

            config.db_close()
            del db_session
            cycle_count = cycle_count + 1
            if cycle_count >= config.delete_cycle_interval:
                delete_cycle = True
                cycle_count = 0
            wait_cycle(cycle_start_time, poll_time_history, config.sleep_interval_job)

    except Exception as exc:
        logging.exception("Job Poller while loop exception, process terminating...")
        logging.error(exc)
        config.db_close()
        del db_session

def command_poller():
    multiprocessing.current_process().name = "Command Poller"

    config = Config('/etc/cloudscheduler/cloudscheduler.yaml', os.path.basename(sys.argv[0]), pool_size=4)
    Job = config.db_map.classes.condor_jobs
    GROUPS = config.db_map.classes.csv2_groups

    try:
        while True:
            logging.info("Beginning command consumer cycle")
            config.db_open()
            db_session = config.db_session
            groups = db_session.query(GROUPS)
            condor_hosts_set = set() # use a set here so we dont re-query same host if multiple groups have same host
            for group in groups:
                # for containers we will have to issue the commands directly to the container and not the condor fqdn so here it takes precedence 
                if group.htcondor_container_hostname is not None and group.htcondor_container_hostname != "":
                    condor_hosts_set.add(group.htcondor_container_hostname)
                else:
                    condor_hosts_set.add(group.htcondor_fqdn)

            uncommitted_updates = 0
            for condor_host in condor_hosts_set: 
                try:
                    coll = htcondor.Collector(condor_host)
                    scheddAd = coll.locate(htcondor.DaemonTypes.Schedd, condor_host)
                    condor_session = htcondor.Schedd(scheddAd)
                except Exception as exc:
                    logging.warning("Failed to locate condor daemon, skipping: %s" % condor_host)
                    logging.debug(exc)
                    continue

                #Query database for any entries that have a command flag
                abort_cycle = False
                for job in db_session.query(Job).filter(Job.hold_job_reason != None):
                    logging.info("Holding job %s, reason=%s" % (job.global_job_id, job.hold_job_reason))
                    local_job_id = job.global_job_id.split('#')[1]
                    try:
                        condor_session.edit([local_job_id,], "JobStatus", "5")
                        condor_session.edit([local_job_id,], "HoldReason", '"%s"' % job.hold_job_reason)

                        job.job_status = 5
                        job.hold_job_reason = None
                        db_session.merge(job)
                        uncommitted_updates = uncommitted_updates + 1

                        if uncommitted_updates >= config.batch_commit_size:
                            try:
                                db_session.commit()
                                uncommitted_updates = 0
                            except Exception as exc:
                                logging.error("Failed to commit batch of job changes, aborting cycle...")
                                logging.error(exc)
                                abort_cycle = True
                                break

                    except Exception as exc:
                        logging.error("Failed to hold job, rebooting command poller...")
                        logging.error(exc)
                        exit(1)

                if abort_cycle:
                    del condor_session
                    config.db_close()
                    del db_session
                    time.sleep(config.sleep_interval_command)
                    continue

            if uncommitted_updates > 0:
                try:
                    db_session.commit()
                except Exception as exc:
                    logging.error("Failed to commit job changes, aborting cycle...")
                    logging.error(exc)
                    del condor_session
                    config.db_close()
                    del db_session
                    time.sleep(config.sleep_interval_command)
                    continue

            logging.info("Completed command consumer cycle")
            config.db_close()
            time.sleep(config.sleep_interval_command)

    except Exception as exc:
        logging.exception("Job poller while loop exception, process terminating...")
        logging.error(exc)
        del condor_session
        db_session.close()


def service_registrar():
    multiprocessing.current_process().name = "Service Registrar"

    # database setup
    db_category_list = [os.path.basename(sys.argv[0]), "general"]
    config = Config('/etc/cloudscheduler/cloudscheduler.yaml', db_category_list, pool_size=4)
    SERVICE_CATALOG = config.db_map.classes.csv2_service_catalog

    service_fqdn = socket.gethostname()
    service_name = "csv2-jobs"

    while True:
        config.db_open()

        service_dict = {
            "service":             service_name,
            "fqdn":                service_fqdn,
            "last_updated":        None,
            "yaml_attribute_name": "cs_condor_remote_job_poller"
        }
        service = SERVICE_CATALOG(**service_dict)
        try:
            config.db_session.merge(service)
            config.db_close(commit=True)
        except Exception as exc:
            logging.exception("Failed to merge service catalog entry, aborting...")
            logging.error(exc)
            return -1
        time.sleep(config.sleep_interval_registrar)

    return -1


if __name__ == '__main__':

    process_ids = {
        'command':   command_poller,
        'job':       job_poller,
        'registrar': service_registrar,
    }

    procMon = ProcessMonitor(file_name=os.path.basename(sys.argv[0]), pool_size=4, orange_count_row='csv2_jobs_error_count', process_ids=process_ids)
    config = procMon.get_config()
    logging = procMon.get_logging()
    version = config.get_version()

    logging.info("**************************** starting csjobs - Running %s *********************************" % version)

    # Wait for keyboard input to exit
    try:
        #start processes
        procMon.start_all()
        while True:
            procMon.check_processes()
            time.sleep(config.sleep_interval_main_long)
            
    except (SystemExit, KeyboardInterrupt):
        logging.error("Caught KeyboardInterrupt, shutting down threads and exiting...")

    except Exception as ex:
        logging.exception("Process Died: %s", ex)

    procMon.join_all()


