import inspect


class DIEntry():

    def __init__(self, name, creator: callable):
        self.name = name
        self.creator = creator

    def create(self):
        return self.creator()


class DIEntryPool():
    '''Pool for dependency injection'''

    __entries = {}

    def get(self, key) -> callable:
        """Obtain object with injected dependencies"""

        key = self.__normalize_key(key)

        if not key in self.__entries:
            raise KeyError('Key {} not found.'.format(key))

        value = self.__entries[key]

        if isinstance(value, DIEntry):
            value = value.create()
            self.__entries[key] = value

        return value

    def add(self, entry: DIEntry):
        """Add object to dependecies storage"""

        name = entry.name
        if not entry.name:
            raise KeyError('Invalid name for DI entry')

        main_key = self.__normalize_key(name)

        self.__entries[main_key] = entry


    def __normalize_key(self, key) -> str:
        if inspect.isclass(key):
            key = key.__name__

        if not isinstance(key, str):
            raise KeyError(f'Key should be a string or class. Error for key: {key}')

        return key


container = DIEntryPool()
