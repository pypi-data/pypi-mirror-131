import logging
import os


class logger:

    LOG_LEVEL = str(os.environ.get("LOG_LEVEL", "info").isupper())
    if LOG_LEVEL not in list(logging._nameToLevel.keys()):
        LOG_LEVEL = "INFO"

    loggers = logging.getLogger("logging")
    logHandler = logging.StreamHandler()
    source_loggers = "application"
    version = "1"
    formate_loggers = (
        "{"
        + f"'timestamp':'%(asctime)s','level':'%(levelname)s','message':'%(message)s','log.source':'{source_loggers}','log.version':{version}"
        + "}"
    )
    formatter = logging.Formatter(formate_loggers, "%Y-%m-%dT%H:%M:%SZ")
    logHandler.setFormatter(formatter)
    logHandler.setLevel(LOG_LEVEL)
    loggers.addHandler(logHandler)

    analyzers = logging.getLogger("analyzer")
    logHandler = logging.StreamHandler()
    source_analyzer = "analyzer"
    version = "1"
    formate_analyzer = (
        "{"
        + f"'timestamp':'%(asctime)s','level':'%(levelname)s','message':%(message)s,'log.source':'{source_analyzer}','log.version':{version}"
        + "}"
    )
    formatter = logging.Formatter(formate_analyzer, "%Y-%m-%dT%H:%M:%SZ")
    logHandler.setFormatter(formatter)
    logHandler.setLevel("INFO")
    analyzers.addHandler(logHandler)

    @classmethod
    def logging(cls):
        return cls.loggers

    @classmethod
    def analyzer(cls):
        return cls.analyzers
