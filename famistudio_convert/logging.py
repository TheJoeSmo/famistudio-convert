from logging import NullHandler, getLogger

LOGGER_NAME = "FSC"

log = getLogger(LOGGER_NAME)
log.addHandler(NullHandler())


def set_log_level(level: int) -> None:
    log.setLevel(level)
