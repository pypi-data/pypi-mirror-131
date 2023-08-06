from .ini_formatter import INI_Formatter
from .json_formatter import JSON_Formatter
from .exceptions import NoExtensionError, NoFormatterError


class FormatFactory:
    def __init__(self):
        self._formatters = {
            "ini": INI_Formatter,
            "json": JSON_Formatter,
        }

    def add_formatters(self, file_exts: list, formatter):
        for ext in file_exts:
            self.add_formatter(ext, formatter)

    def add_formatter(self, ext: str, formatter):
        self._formatters[ext] = formatter

    def remove_formatter(self, ext):
        self._formatters.pop(ext, None)

    def get_formatter(self, filepath):
        if not filepath:
            raise NoExtensionError()
        else:
            try:
                ext = str(filepath.name)
            except AttributeError:
                ext = filepath
            d = ext.split('.')
            if len(d) > 1:
                ext = d[1]
        if ext not in self._formatters:
            raise NoFormatterError(ext=ext)
        return self._formatters[ext]()
