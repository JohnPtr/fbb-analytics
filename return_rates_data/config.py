import os

class Config:
    SF_DRIVER = os.getenv("SF_DRIVER", "")
    SF_UID = os.getenv("SF_UID", "")
    SF_PWD = os.getenv("SF_PWD", "")
    SF_SERVER = os.getenv("SF_SERVER", "")
    SF_DATABASE = os.getenv("SF_DATABASE", "")
    SF_SCHEMA = os.getenv("SF_SCHEMA", "")
    SF_WAREHOUSE = os.getenv("SF_WAREHOUSE", "")
    SF_ROLE = os.getenv("SF_ROLE", "")
