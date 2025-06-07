import logging

def get_logger(name,file='server.log',level=logging.DEBUG):
    logger = logging.getLogger(name)

    logger.setLevel(level)
    file_handler = logging.FileHandler(file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger