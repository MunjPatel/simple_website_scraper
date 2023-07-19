import logging
import colorlog
import os
import sys

class Logger:
    """
    
    General class for all logging messages.

    """

    def __init__(self)->None:
        pass
    def get_logger(self) -> None:
        """
            
        Logger object to be initiated to start logging of messages.

        Input: self
        Output: None
            
        """
    global logger
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    global logger_variable
    logger_variable = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(logger_variable, exist_ok=True)
    log_file = os.path.join(logger_variable, "process.log")
    fh = logging.FileHandler(log_file)
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s [%(asctime)s] - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    logger.addHandler(sh)

    # def get_logger(self)->None:
    #     """
        
    #     Logger object to be initiated to start logging of messages.

    #     Input: self
    #     Output: None
        
    #     """
    #     global logger
    #     logger = logging.getLogger('')
    #     logger.setLevel(logging.INFO)
    #     global logger_variable
    #     logger_variable = os.path.join(os.path.dirname(__file__), '..', 'logs')
    #     log_file = os.path.join(logger_variable, "process.log")
    #     fh = logging.FileHandler(log_file)
    #     sh = logging.StreamHandler(sys.stdout)
    #     formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
    #     fh.setFormatter(formatter)
    #     sh.setFormatter(colorlog.ColoredFormatter(
    #         '%(log_color)s [%(asctime)s] - %(levelname)s - %(message)s'))
    #     logger.addHandler(fh)
    #     logger.addHandler(sh)

    def get_info(self, arg:str)->str:
        """
        
        Logs information message and returns it as a string.

        Input: self
        Output: str
        
        """
        return logger.info(arg)
    
    def get_warning(self, arg:str)->str:
        """
        
        Logs warning message and returns it as a string.

        Input: self
        Output: str
        
        """
        return logger.warning(arg)


    def get_critical(self, arg:str)->str:
        """
        
        Logs critical message and returns it as a string.

        Input: self
        Output: str
        
        """
        return logger.critical(arg)
    
    def clear_logs(self)->str:
        """
        
        Clears all the previous data stored in the log file and resets it. This function is called everytime the scraper.py file is run.

        Input: None
        Output: str
        
        """
        with open(logger_variable+"/process.log","w"):
            pass
        return "Previous data cleared."
    
# log_instance = Logger()
# log_instance.get_logger()
# log_instance.get_critical("This is a critical message!")