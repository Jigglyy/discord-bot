import sys
import logging
from loguru import logger
from datetime import datetime
import datetime


def configure_logger():
    
    logger.remove()
    # Configure logging to stderr with the desired format and level
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        
    )
    

    # Configure loguru to use the same logging handlers as the root logger
    today = datetime.date.today().strftime("%Y-%m-%d")
    log_filename = f"file_{today}.log"
    format = "<red>{level}</red> || <green>{time:DD-MM-YYYY HH:mm:ss}</green> || <level><yellow>{module}>{file}</yellow></level> || <blue>{message}</blue>"
    logger.remove()
    logger.add(logging.StreamHandler(sys.stderr), colorize=True, format=format)
    logger.add(log_filename,  level="DEBUG", rotation="10 MB", format=format)
    
    # Return the logger
    return logger