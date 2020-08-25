from pathlib import Path


class RequireEnvInjector(object):
    def __init__(self, next_injector):
        self.next_injector = next_injector

    def __call__(self, path_s, code):
        from .pydyimport import DynamicImport
        obj = DynamicImport(Path(path_s).relative_to(DynamicImport.ROOTDIR))
        result = {
            'require': obj.require,
            'require_only': obj.require_only,
        }
        if self.next_injector:
            result.update(self.next_injector(path_s, code))
        return result
