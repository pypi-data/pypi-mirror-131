from . import create_configuration, load
import pathlib
import os


class Configuration:
    def __init__(self, location='', defaults={}, load_env=False, _parent=None):
        self._parent = _parent
        self._location = self.__set_location(location)
        self.load_env = load_env
        self._data = defaults.copy()
        self._data_loaded=False

    """items()

    """
    def items(self):
        return self._data.items()

    """valueOf(name, default=None, type_=None)

    get the value of a configuration value by  name.

    If config does not contain the key, default will be returned.

    To ensure that the returned value is a certain type (such as str or int),
    pass the type to the type_ argument. This will return None if property is not
    set and default is set to None.
    """
    def valueOf(self, name, default=None, type_=None):
        value = self._data.get(name, default) # Get the value or default from config
        if type_ and isinstance(type_, type): # If it is not None and needs to be a certain type
            print(type(value), value)
            if value and not isinstance(value, type_):
                value = type_(value) #Cast value as type
        elif isinstance(value, dict): # Dont return a dict, unless expressly told to.
            conf = create_configuration(filepath='', _parent=self, load_env=self.load_env)
            conf._data = value
            conf._data_loaded = True #Return a new instance of SimpleConfig
            value = conf
        return value #Return the value.

    """Reload()

    Reload the configuration From file and/or environment, updating configuration if
    the file/environment has changed.
    """
    def reload(self):
        self = load(self)

    def remove(self, key):
        pass

    def __str__(self):
        return str("<Configuration data: %s >"%self._data)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self._data.__iter__()

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        pass

    def __set_location(self, location):
        if os.name == 'nt':  # Set Windows Path
            return pathlib.WindowsPath(location)
        else:  # Set Posix Path
            return pathlib.PosixPath(location)
