import multiprocessing
from multiprocessing import Process
import logging
import time
import sys
import os
import psutil

from cloudscheduler.lib.db_config import *

from cloudscheduler.lib.poller_functions import \
    start_cycle, \
    wait_cycle

import htcondor
import classad
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


def _service_msg(service_name):
    return os.popen("service "+service_name+" status | grep 'Active' | cut -c12-").read() 

def status_poller():
    multiprocessing.current_process().name = "Status Poller"

    services = ["csv2-main", "csv2-openstack", "csv2-jobs", "csv2-machines", "mariadb", "condor"]
    db_service_names = {
                       "csv2-main":      "csv2_main", 
                       "csv2-openstack": "csv2_openstack", 
                       "csv2-jobs":      "csv2_jobs", 
                       "csv2-machines":  "csv2_machines", 
                       "mariadb":        "mariadb", 
                       "condor":         "condor"
                   }

    # Initialize database objects
    Base = automap_base()
    db_engine = create_engine(
        'mysql://%s:%s@%s:%s/%s' % (
            config.db_config['db_user'],
            config.db_config['db_password'],
            config.db_config['db_host'],
            str(config.db_config['db_port']),
            config.db_config['db_name']
            )
        )
    Base.prepare(db_engine, reflect=True)
    STATUS = Base.classes.csv2_system_status

    db_session = Session(db_engine)

    cycle_start_time = 0
    new_poll_time = 0
    poll_time_history = [0,0,0,0]

    try:
        while True:
            new_poll_time, cycle_start_time = start_cycle(new_poll_time, cycle_start_time)
            # id will always be zero because we only ever want one row of these
            system_dict = {'id': 0}
            for service in services:
                system_dict[db_service_names[service] + "_msg"] = _service_msg(service)
                if "running" in system_dict[db_service_names[service] + "_msg"]:
                    system_dict[db_service_names[service] + "_status"] = 1
                else:
                    system_dict[db_service_names[service] + "_status"] = 0

                system_dict["load"] = round(100*( os.getloadavg()[0] / os.cpu_count() ),1)

                system_dict["ram"] = psutil.virtual_memory().percent
                system_dict["ram_size"] = round(psutil.virtual_memory().total/1000000000 , 1)
                system_dict["ram_used"] = round(psutil.virtual_memory().used/1000000000 , 1)

                system_dict["swap"] = psutil.swap_memory().percent
                system_dict["swap_size"] = round(psutil.swap_memory().total/1000000000 , 1)
                system_dict["swap_used"] = round(psutil.swap_memory().used/1000000000 , 1)


                system_dict["disk"] = round(100*(psutil.disk_usage('/').used / psutil.disk_usage('/').total),1)
                system_dict["disk_size"] = round(psutil.disk_usage('/').total/1000000000 , 1)
                system_dict["disk_used"] = round(psutil.disk_usage('/').used/1000000000 , 1)

            new_status = STATUS(**system_dict)
            try:
                db_session.merge(new_status)
                db_session.commit()
            except Exception as exc:
                logging.exception("Failed to merge and commit status update exiting")
                exit(1)

            wait_cycle(cycle_start_time, poll_time_history, config.sleep_interval_status)
    except Exception as exc:
        logging.exception("Problem during general execution:")
        logging.exception(exc)
        logging.error("Exiting..")
        exit(1)


if __name__ == '__main__':
    # old config
    #config = Config(os.path.basename(sys.argv[0]))
    config = Config(os.path.basename(sys.argv[0]), db_config_dict=True)

    logging.basicConfig(
        filename=config.log_file,
        level=config.log_level,
        format='%(asctime)s - %(processName)-14s - %(levelname)s - %(message)s')

    logging.info("**************************** starting csstatus *********************************")

    processes = {}
    process_ids = {
        'status': status_poller,
        }

    # Wait for keyboard input to exit
    try:
        while True:
            for process in sorted(process_ids):
                if process not in processes or not processes[process].is_alive():
                    if process in processes:
                        logging.error("%s process died, restarting...", process)
                        del(processes[process])
                    else:
                        logging.info("Restarting %s process", process)
                    processes[process] = Process(target=process_ids[process])
                    processes[process].start()
                    time.sleep(config.sleep_interval_main_short)
            time.sleep(config.sleep_interval_main_long)
    except (SystemExit, KeyboardInterrupt):
        logging.error("Caught KeyboardInterrupt, shutting down threads and exiting...")

    for process in processes:
        try:
            process.join()
        except:
            logging.error("failed to join process %s", process)
