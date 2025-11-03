import logging

class xLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def log(self, message: str, level: str = "info"):
        self.logger.log(logging._nameToLevel.get(level.upper(), 1), message)


    def debug(self, message: str):
        self.log(message, level="debug")

    def info(self, message: str):
        self.log(message, level="info")

    def warning(self, message: str):
        self.log(message, level="warning")

    def error(self, message: str):
        self.log(message, level="error")

    def critical(self, message: str):
        self.log(message, level="critical")


xlogger = xLogger(__name__)
