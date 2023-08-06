import configparser
from .formatbase import FormatterBase

class INI_Formatter(FormatterBase):
    def __init__(self, interpolation=configparser.BasicInterpolation()):
        super().__init__()
        self.interpolation=interpolation
    def write(self, file, data):
        parser = configparser.ConfigParser(interpolation=self.interpolation)
        writeData = data.copy()
        for k,v in data.items():
            if isinstance(v, list):
                raise Exception('INI formatter deos not support lists!')
        for k,v in writeData.items():
            if not isinstance(v, dict):
                writeData = { 'configuration': writeData }
                break
        parser.optionxform=str
        parser.read_dict(writeData)
        return parser.write(file)
    def read(self, file):
        parser = configparser.ConfigParser(interpolation=self.interpolation)
        parser.optionxform=str
        parser.read_file(file)
        if len(parser.sections()) == 1 and 'configuration' in parser.sections():
            return parser['configuration']
        return parser._sections
