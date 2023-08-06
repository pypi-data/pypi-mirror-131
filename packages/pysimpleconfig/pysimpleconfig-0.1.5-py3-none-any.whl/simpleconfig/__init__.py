'''Simple Configuration
A simple configuration library.
This library facilitates easily handling and managing changable and non-changeable configurations.
'''
# TODO: Expand documentation for simpleconfig

from simpleconfig.formatters.exceptions import NoExtensionError, NoFormatterError
from .formatters import FormatFactory
from blinker import signal
from os import path, environ, makedirs
from .formatters import JSON_Formatter, INI_Formatter, NoFormatterError, NoExtensionError, FormatterBase, FormatFactory

_formatters = FormatFactory()

on_update = signal('simpleconfig_on_update')
"""
Blinker signal will call all registered functions whenever an updatable configuration has a change.
Function is required to handle the following args: configuration, action, key, old_value, new_value

configuration - Configuration object that updated.
action - "set" if key was not present.
         "updated" if key was present and new value assigned
         "removed" if key and value removed from configuration
key - The named setting updated in configuration
old_value - The value that is no longer assigned to key, unless action is "set" then it is None.
new_value - The new value assigned to key, unless action is "removed" then it is None.

use:

    import simpleconfig

    def my_func(configuration, action, key, old_value, new_value):
        # do checks, update configuration, log actions
        pass

    simpleconfig.on_update.connect(my_func)

    settings = simpleconfig.load_or_create(filepath='.', defaults={}, updatable=True)

    settings['new_key'] = 'set action'
 
"""

on_save = signal('simpleconfig_on_save')

on_load = signal('simpleconfig_on_load')


def create_configuration(filepath='', defaults={}, load_env=False, _parent=None, **kwargs):
    """
    Factory to create Configuration Objects

    Paramters:

    filepath - Path to location of desired or existing configuration file

    defaults - A dict containing default configuration. These will be overwritten by any loaded configuration.

    load_env - If True, simpleconfig will search for each key in defaults dict for configuration settings set in system
    environment.

    _parent - Do not use, used for internal mapping.


    returns Configuration Object

    """
    from .configuration import Configuration
    return Configuration(location=str(filepath), _parent=_parent, defaults=defaults, load_env=load_env)


def create_settings(filepath='', defaults={}, load_env=False, auto_save=False, _parent=None):
    """
    Factory to create Settings Objects

    Paramters:

    filepath - Path to location of desired or existing configuration file

    defaults - A dict containing default configuration. These will be overwritten by any loaded configuration.

    load_env - If True, simpleconfig will search for each key in defaults dict for configuration settings set in system
    environment.

    _parent - Do not use, used for internal mapping.

    auto_save - If true, configuration will be saved whenever a setting is changed.

    returns Settings Object

    """
    from .settings import Settings
    return Settings(location=str(filepath), defaults=defaults, load_env=load_env,
                    auto_save=auto_save, _parent=_parent)


def load_or_create(filepath='', defaults={}, load_env=False, updatable=False, auto_save=False):
    """
    Factory to load a configuration or to create one if not present at given location.

    filepath - Path to location of desired or existing configuration file
    defaults - A dict containing default configuration. These will be overwritten by any loaded configuration.
    load_env - If True, simpleconfig will search for each key in defaults dict for configuration settings set in system
                environment.
    updatable - If this configuration should be changable, set this to True.
        Will return a Settings object if True.
    auto_save - If this configuration should save when it is updated.
        Assumes updatable is True and will return Settings object.

    returns Configuration object or Settings object if updatable or auto_save is True.

    """
    if updatable or auto_save:
        factory = create_settings
    else:
        factory = create_configuration
    if filepath:
        configuration = factory(filepath=filepath, defaults=defaults, load_env=load_env, auto_save=auto_save)
        configuration = load(configuration)
        if not path.exists(str(filepath)):
            save(configuration)
    elif defaults:
        configuration = factory(filepath=filepath, defaults=defaults, load_env=load_env, auto_save=auto_save)
        if load_env:
            configuration = load(configuration)
    else:
        raise Exception("No Data for configuration")
    return configuration


def load(configuration):
    load_env = configuration.load_env
    configuration._data_loaded = False
    # If the configuration is set to load from env
    if load_env:
        configuration = _load_env(configuration=configuration)
    # Load the configuration from file
    if configuration._location:
        configuration = _load_file(filepath=configuration._location, configuration=configuration)
    configuration._data_loaded = True
    on_load.send(sender=configuration)
    return configuration


def save(configuration):
    on_save.send(sender=configuration)
    filepath = configuration._location
    if not filepath:
        return False
    try:
        formatter = _formatters.get_formatter(filepath=filepath)
    except (NoExtensionError, NoFormatterError):
        return False
    makedirs(path.join(filepath.parents[0]), exist_ok=True)
    with open(filepath, 'w+') as f:
        formatter.write(file=f, data=configuration._data)
    return True


def _load_env(configuration):
    data={}
    for k in configuration._data.keys():
        if k in environ:
            data[k] = environ[k]
    configuration._data.update(data)
    return configuration


def _load_file(filepath, configuration):
    if not path.exists(filepath):
        return configuration
    try:
        formatter = _formatters.get_formatter(filepath=filepath)
    except (NoFormatterError, NoExtensionError):
        return configuration
    data={}
    with open(filepath, formatter.readMode) as configFile:
        data = formatter.read(configFile)
    configuration._data.update(data)
    return configuration


def get_formatter(filepath):
    global _formatters
    return _formatters.get_formatter(filepath)


def remove_formatter(ext):
    global _formatters
    return _formatters.remove_formatter(ext)


def add_formatter(file_exts: list, formatter):
    global _formatters
    return _formatters.add_formatter(file_exts, formatter)


from .configuration import Configuration
from .settings import Settings
