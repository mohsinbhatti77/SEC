import os
import sys
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from networksec.Logging.logger import logger
from networksec.customexception.exception import NetworkSecurityException


class ModelTrainer:
    def __init__(self, df, target_column="Result", model_output_path="models/model.pkl"):
        try:
            self.df = df
            self.target_column = target_column
            self.model_output_path = model_output_path

            self.X = df.drop(columns=[target_column])
            self.y = df[target_column]

            logger.info("ModelTrainer initialized successfully.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data(self, test_size=0.2, random_state=42):
        try:
            self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
                self.X, self.y, test_size=test_size, random_state=random_state
            )
            logger.info(f"Data split into train and validation sets. Train shape: {self.X_train.shape}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_random_forest(self):
        try:
            self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
            self.model.fit(self.X_train, self.y_train)
            logger.info("Random Forest model trained successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def evaluate_model(self):
        try:
            predictions = self.model.predict(self.X_val)
            acc = accuracy_score(self.y_val, predictions)
            report = classification_report(self.y_val, predictions)
            logger.info(f"Accuracy: {acc:.4f}")
            logger.info(f"Classification Report:\n{report}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def save_model(self):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            joblib.dump(self.model, self.model_output_path)
            logger.info(f"Model saved at {self.model_output_path}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
