from config.mongoconfig import MongoDBConnection
from networksec.preprocessing import DataPreprocessor
from networksec.model_training import ModelTrainer
from networksec.Logging.logger import logger

uri = "mongodb+srv://mohsinking998877:bhatti123@cluster0.5enc7va.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_name = "SEC"
collection_name = "SEC"

# Step 1: Preprocess
preprocessor = DataPreprocessor(uri, db_name, collection_name)
df_clean = preprocessor.clean_data()

# Step 2: Train
trainer = ModelTrainer(df_clean)
trainer.split_data()
trainer.train_random_forest()
trainer.evaluate_model()
trainer.save_model()

logger.info("✅ Model training workflow completed.")





