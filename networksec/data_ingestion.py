import pandas as pd
import os
import sys

from networksec.Logging.logger import logging
from networksec.customexception.exception import NetworkSecurityException
from config.mongoconfig import MongoDBConnection

class DataIngestion:
    def __init__(self, uri: str, db_name: str, collection_name: str, file_path: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.file_path = file_path

    def load_data(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"{self.file_path} does not exist.")
            
            df = pd.read_csv(self.file_path)
            logging.info(f"Loaded data from {self.file_path} with shape {df.shape}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_to_mongo(self, df):
        try:
            mongo_conn = MongoDBConnection(self.uri)
            client = mongo_conn.connect()

            db = client[self.db_name]
            collection = db[self.collection_name]

            data_dict = df.to_dict(orient="records")
            result = collection.insert_many(data_dict)

            logging.info(f"Inserted {len(result.inserted_ids)} records into {self.db_name}.{self.collection_name}")
            print(f"Data inserted successfully into MongoDB.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run(self):
        try:
            df = self.load_data()
            self.insert_to_mongo(df)
        except NetworkSecurityException as ne:
            logging.error(f"Data ingestion failed: {ne}")
        except Exception as e:
            logging.error(f"Unknown error during ingestion: {str(e)}")

