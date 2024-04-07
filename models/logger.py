from datetime import datetime
import json
import logging
import os
from libs.decimalencoder import DecimalEncoder
class Log:
    logger = None
    def __init__(self, file_name, level):
        logging.basicConfig(filename=file_name, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=level)
        self.logger = logging.getLogger(file_name)
