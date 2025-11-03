import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)

class xLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()

        formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
