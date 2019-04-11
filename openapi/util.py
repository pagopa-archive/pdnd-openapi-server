import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("openapi")


def loggable(wrapped):
    @wraps(wrapped)
    def t(*args, **kwds):
        try:
            log.info(
                "{fname}({args}, {kwds}".format(
                    fname=wrapped.__name__, args=args, kwds=kwds
                )
            )
        except Exception:
            log.exception(wrapped)

        return wrapped(*args, **kwds)

    return t
