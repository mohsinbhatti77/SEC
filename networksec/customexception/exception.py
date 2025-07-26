# networksec/customexception/exception.py

import sys
from networksec.Logging.logger import logger

class NetworkSecurityException(Exception):
    """Custom exception class that logs traceback info"""
    
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error(error_message, error_details)

        logger.error(self.error_message)  # Log on instantiation

    def get_detailed_error(self, error_message, error_details: sys):
        _, _, exc_tb = error_details.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        return f"Error in script [{file_name}] at line [{line_number}]: {error_message}"

    def __str__(self):
        return self.error_message
