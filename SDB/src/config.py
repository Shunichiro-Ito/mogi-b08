from dotenv import load_dotenv
import os
IS_IN_DOCKER = os.path.exists("../.dockerenv")
if not IS_IN_DOCKER:
    load_dotenv()
print("is_in_docker", IS_IN_DOCKER)

try:
    URL_DB = os.environ.get("URL_DB")
    if URL_DB is None:
        raise Exception("URL_DB not found")
    IS_IN_DOCKER = True
except:
    DB_USER = os.environ.get("DB_USER")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")
    DATABASE = os.environ.get("DATABASE")
    SERVICE = os.environ.get("SERVICE")
    PORT = os.environ.get("PORT")

RESET = os.environ.get("RESET")
if RESET == "True":
    RESET = True
else:
    RESET = False
print("RESET", RESET)

