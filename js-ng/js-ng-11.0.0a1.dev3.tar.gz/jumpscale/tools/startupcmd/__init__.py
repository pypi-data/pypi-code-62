def export_module_as():
    from jumpscale.core.base import StoredFactory
    from .startupcmd import StartupCmd

    return StoredFactory(StartupCmd)
