import logging


class Loggers(object):

    def __init__(self, file_name):
        self.logger = logging.getLogger(file_name)
        self.hdlr = logging.FileHandler(file_name + '.log')
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


def log(file_name):
    return Loggers(file_name)
