try:
    import logbook
    log = logbook
except ImportError:
    import logging
    log = logging.getLogger("vtb.cloudsdk")

