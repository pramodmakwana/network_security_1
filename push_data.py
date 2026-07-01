import os
import sys
import json
import collections
import collections.abc
# Monkey-patch for older bson/pymongo versions running on newer Python
collections.MutableMapping = collections.abc.MutableMapping

from dotenv import load_dotenv
load_dotenv()

# Read env variable name correctly
MONGODB_URL = os.getenv("MONGO_DB_URL")
print(f"MongoDB URL loaded: {MONGODB_URL}")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging

class NetworkdataExtractor:
    def __init__(self):
        pass
        
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)  
            data.reset_index(drop=True, inplace=True)
            # Converts dataframe to a list of JSON records (dictionaries)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def push_data_to_mongodb(self, records: list, database_name: str, collection_name: str):
        try:
            self.database_name = database_name
            self.collection_name = collection_name
            self.records = records

            # Added the certifi tlsCAFile argument to prevent SSL connection issues
            self.mongo_client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]
            
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH = os.path.join("C:\\Users\\pramod makwana\\Desktop\\Data science\\network secrity project 1\\Network_Data\\phisingData.csv")
    DATABASE_NAME = "pramodAI"
    COLLECTION_NAME = "network_data"
    
    # Consistent variable usage:
    network_obj = NetworkdataExtractor()
    
    # Catching the return values explicitly
    records = network_obj.csv_to_json_converter(file_path=FILE_PATH)
    print(f"Total processed records extracted: {len(records)}")
    
    no_of_records = network_obj.push_data_to_mongodb(
        records=records, 
        database_name=DATABASE_NAME, 
        collection_name=COLLECTION_NAME
    )
    print(f"Successfully inserted {no_of_records} records into MongoDB.")