
import logging
from config import *

FOLDER = "logs"

class Log():
    def __init__(self, filename):
        self.filename = FOLDER + "/" + filename
        
        logging.basicConfig(
            filename=self.filename,
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        self.logger = logging.getLogger(filename.replace(".log", ""))
        self.logger.setLevel(logging.DEBUG)

        self.filehandler = logging.FileHandler(self.filename)
        self.filehandler.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
        self.filehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.filehandler)

    def log(self, level, msg):
        if level is LogLevels.INFO.value:
            self.logger.info(msg)
        elif level is LogLevels.WARNING.value:
            self.logger.warning(msg)
        elif level is LogLevels.ERROR.value:
            self.logger.error(msg)

    
