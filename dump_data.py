import pymongo
import pandas as pd
import json


client = pymongo.MongoClient("mongodb+srv://muky:LIRnBEt7144wkn9Y@cluster0.ufqox21.mongodb.net/?retryWrites=true&w=majority")

FILE_PATH_NAME="/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME="aps"
COLLECTION_NAME="sensor"

if __name__=="__main__":
    df=pd.read_csv(FILE_PATH_NAME)
    print(f"row and column:{df.shape}")

    df.reset_index(drop=True,inplace=True)

    json_record=list(json.loads(df.T.to_json()).values())
    print(json_record[0])
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)