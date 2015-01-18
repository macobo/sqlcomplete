from .version import __version__


def setup_logger():
    import logging
    _logger = logging.getLogger('sqlcomplete')
    _logger.addHandler(logging.NullHandler())

setup_logger()