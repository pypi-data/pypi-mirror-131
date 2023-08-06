from .configuration import Configuration
from . import on_update, save


class Settings(Configuration):
    def __init__(self, location='', defaults={}, load_env=False, auto_save=False, _parent=None,):
        super().__init__(location, defaults, load_env, _parent)
        self.on_update = on_update
        self.on_update.connect(self._save)
        self.auto_save = auto_save

    def setValue(self, key, value):
        val = self._data.get(key)
        self._data[key] = value
        if val:
            self._notify('updated', key=key, old_value=val, new_value=value)
        else:
            self._notify('set', key=key, new_value=value)

    def remove(self, key):
        val = self._data.pop(key)
        if val:
            self._notify('removed', key=key, old_value=val)

    def _save(self, *args, **kwargs):
        if self.auto_save:
            save(self)

    def _notify(self, action, key, old_value=None, new_value=None):
        if self._data_loaded:
            self._data_loaded = False
            on_update.send(self, action=action, key=key, old_value=old_value, new_value=new_value)
            self._data_loaded = True

    def __setitem__(self, key, value):
        self.setValue(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __str__(self):
        return str("<Settings data: %s >" % self._data)
