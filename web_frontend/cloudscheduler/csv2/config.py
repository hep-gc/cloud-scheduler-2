import os
import sys
import yaml


db_host = "localhost"
db_port = 3306
db_user = "csv2"
db_password = ""
log_file_path = "/var/log/cloudscheduler/csv2_web.log"
enable_glint = False

if os.path.isfile("/etc/cloudscheduler/cloudscheduler.yaml"):
    path = "/etc/cloudscheduler/cloudscheduler.yaml"

elif os.path.isfile("/opt/cloudscheduler/web_frontend/cloudscheduler/conf/cloudscheduler.yaml"):
    path = "/opt/cloudscheduler/web_frontend/cloudscheduler/conf/cloudscheduler.yaml"


try:
    with open(path, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

except Exception as e:
    print(" Configuration file problem: There was a " \
          "problem reading %s. Check that it is readable," \
          "and that it exists. " % path, file=sys.stderr)



if "database" in cfg:
    if "db_host" in cfg["database"]:
        db_host = cfg["database"]["db_host"]

    if "db_port" in cfg["database"]:
        db_port = cfg["database"]["db_port"]

    if "db_name" in cfg["database"]:
        db_name = cfg["database"]["db_name"]

    if "db_user" in cfg["database"]:
        db_user = cfg["database"]["db_user"]

    if "db_password" in cfg["database"]:
        db_password = cfg["database"]["db_password"]


if "general" in cfg:
    if "log_file_path" in cfg["general"]:
        log_file_path = cfg["general"]["log_file_path"]

    if "enable_glint" in cfg["general"]:
        enable_glint = bool(cfg["general"]["enable_glint"])

