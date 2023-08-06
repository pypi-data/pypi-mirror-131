# Custom exceptions for simpleconfig


'''NoExtensionError
This error is used in simple config when looking up a formatter
with a filename that doesn't include an extension.'''


class NoExtensionError(Exception):
    def __init__(self):
        super().__init__("No extension on filename, unable to determine formatter.")


'''NoFormatterError
This error is used in simpleconfig when a formatter is not available for given extension.'''


class NoFormatterError(Exception):
    def __init__(self, ext):
        super().__init__("No Formatter for ext: %s" % ext)
        self.ext = ext
