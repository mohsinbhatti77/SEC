import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from networksec.Logging.logger import logger
from networksec.customexception.exception import NetworkSecurityException
from config.mongoconfig import MongoDBConnection


class DataPreprocessor:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name

    def load_data(self):
        try:
            client = MongoDBConnection(self.uri)
            db = client[self.db_name]
            collection = db[self.collection_name]
            data = list(collection.find())
            df = pd.DataFrame(data)
            logger.info("Raw data loaded from MongoDB.")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def clean_data(self):
        try:
            df = self.load_data()
            if '_id' in df.columns:
                df.drop(columns=['_id'], inplace=True)
            logger.info("Data cleaned successfully.")
            print("Preprocessing Done")
            print(f"X_train shape: {df.drop('Result', axis=1).shape}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def preprocess(self) -> tuple:
        try:
            df = self.fetch_data_from_mongo()
            df = self.clean_data(df)

            X = df.drop("Result", axis=1)
            y = df["Result"]

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42
            )

            logger.info("Data preprocessing complete. Ready for modeling.")
            return X_train, X_test, y_train, y_test, scaler

        except Exception as e:
            logger.error("Error in preprocessing pipeline.")
            raise NetworkSecurityException(e, sys)

