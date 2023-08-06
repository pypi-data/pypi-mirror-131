class FormatterBase(object):
    def __init__(self, writeMode='w+', readMode='r'):
        self._writeMode = writeMode
        self._readMode = readMode
    def write(self, file, data):
        raise NotImplementedError()
    def read(self, file):
        raise NotImplementedError()
    @property
    def writeMode(self):
        return self._writeMode
    @property
    def readMode(self):
        return self._readMode
    @writeMode.setter
    def writeMode(self, x):
        pass
    @readMode.setter
    def readMode(self, x):
        pass
