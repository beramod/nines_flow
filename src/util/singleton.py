class Singleton:
    _instance = None

    @classmethod
    def _get_instance(cls, *args, **kargs):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._get_instance
        return cls._instance