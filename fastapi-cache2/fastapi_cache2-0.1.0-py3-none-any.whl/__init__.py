from fastapi_cache.coder import Coder, JsonCoder


class FastAPICache:
    _backend = None
    _prefix = None

    @classmethod
    def init(cls, backend, prefix: str = ""):
        cls._backend = backend
        cls._prefix = prefix

    @classmethod
    def get_backend(cls):
        assert cls._backend, "You must call init first!"
        return cls._backend

    @classmethod
    def get_prefix(cls):
        assert cls._prefix, "You must call init first!"
        return cls._prefix
