import unittest
import logging, logging.config

logging.config.fileConfig(fname='vision_logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

class LoggerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        logger.debug('Debug')

    def test_something(self):
        print("")


if __name__ == '__main__':
    unittest.main()
