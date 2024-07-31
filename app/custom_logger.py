import sys


class CustomLogger:
    LEVELS = {
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'CRITICAL': 50
    }

    def __init__(self, level='INFO'):
        self.level = self.LEVELS.get(level.upper(), 20)

    def _log(self, level, message):
        if self.LEVELS[level] >= self.level:
            print(f"{level}: {message}\n", file=sys.stderr)

    def debug(self, message):
        self._log('DEBUG', message)

    def info(self, message):
        self._log('INFO', message)

    def warning(self, message):
        self._log('WARNING', message)

    def error(self, message):
        self._log('ERROR', message)

    def critical(self, message):
        self._log('CRITICAL', message)


# Create a global logger instance
logger = CustomLogger()
