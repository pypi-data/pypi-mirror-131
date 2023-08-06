import gevent.monkey
gevent.monkey.patch_all()
from . import common
from loguru import logger


debug = logger.debug
info = logger.info
error = logger.error
warning = logger.warning
exception = logger.exception


