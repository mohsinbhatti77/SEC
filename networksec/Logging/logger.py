import logging
import os
from datetime import datetime

#Define log directory and ensure it exists
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

#Create a timestamped log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

#Logging configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='a',
    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#Create logger instance
logger = logging.getLogger("networksec")
logger.setLevel(logging.INFO)

