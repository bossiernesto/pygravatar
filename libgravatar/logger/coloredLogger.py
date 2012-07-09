import logging
import coloredFormater as c
from abc import ABCMeta

class AbstractLogger(logging.Logger):

    __metaclass__=ABCMeta

    def __init__(self,name):
        raise NotImplementedError


# Custom logger class with multiple destinations
class ColoredLogger(AbstractLogger):
    FORMAT = "[$BOLD%(name)-s$RESET][%(levelname)-s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d) at "
    COLOR_FORMAT = c.formatter_message(FORMAT, True)
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        color_formatter = c.ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        logging.setLoggerClass(ColoredLogger)
        return
