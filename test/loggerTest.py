from libgravatar.logger.coloredLogger import ColoredLogger,AbstractLogger
from unittest import TestCase
import logging

#Mock logger to get messages
class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
            }

class testLogger(TestCase):

    TEST_LOGGER='test'

    def setUp(self):
        self.logger=ColoredLogger(self.TEST_LOGGER)

    def testCallLogger(self):
        self.assertIsInstance(logging.getLogger(self.TEST_LOGGER),ColoredLogger)

    def testLogByName(self):
        log2=logging.getLogger(self.TEST_LOGGER)
        log2.info('Info Test')

    def testLogInfo(self):
        self.logger.info('Info Test')

    def testAbstractLogger(self):
        with self.assertRaises(NotImplementedError):
            abstractLogger=AbstractLogger(name='abstract')