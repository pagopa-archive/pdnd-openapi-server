from functools import wraps
import logging

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
        except Exception as e:
            log.exception(wrapped)

        return wrapped(*args, **kwds)

    return t
