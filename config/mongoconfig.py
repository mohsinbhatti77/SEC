import sys
from pymongo import MongoClient
from networksec.Logging.logger import logging
from networksec.customexception.exception import NetworkSecurityException


class MongoDBConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.client.admin.command("ping")  # Ping to test connection
            logging.info("Connected to MongoDB Atlas.")
            return self.client
        except Exception as e:
            logging.error("MongoDB connection failed.")
            raise NetworkSecurityException(str(e), sys)
