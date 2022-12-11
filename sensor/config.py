import pymongo
import pandas as pd
import json
from dataclasses import dataclass

import os
@dataclass
class EnviromentVariable:

    mongo_db_url:str = os.getenv("MONGO_DB_URL")
    aws_access_key_id:str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key_id:str = os.getenv("AWS_SECRET_KEY_ID")



env_var=EnviromentVariable()

mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "class"