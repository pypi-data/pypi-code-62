import sys
import wasmtime
try:
    from importlib import resources as importlib_resources
    try:
        importlib_resources.files # py3.9+ stdlib
    except AttributeError:
        import importlib_resources # py3.8- shim
except ImportError:
    import importlib_resources # py3.6- shim


def _run_wasm_app(wasm_filename, argv):
    wasm_cfg = wasmtime.Config()
    wasm_cfg.cache = True

    wasi_cfg = wasmtime.WasiConfig()
    wasi_cfg.argv = argv
    wasi_cfg.preopen_dir(str(importlib_resources.files(__package__) / "share"), "/share")
    wasi_cfg.preopen_dir("/", "/")
    wasi_cfg.preopen_dir(".", ".")
    wasi_cfg.inherit_stdin()
    wasi_cfg.inherit_stdout()
    wasi_cfg.inherit_stderr()

    store = wasmtime.Store(wasmtime.Engine(wasm_cfg))
    linker = wasmtime.Linker(store)
    wasi = linker.define_wasi(wasmtime.WasiInstance(store,
        "wasi_snapshot_preview1", wasi_cfg))
    app = linker.instantiate(wasmtime.Module(store.engine,
        importlib_resources.read_binary(__package__, wasm_filename)))
    try:
        app.exports["_start"]()
        return 0
    except wasmtime.ExitTrap as trap:
        return trap.code


def run_icepll(argv):
    return _run_wasm_app("icepll.wasm", ["yowasp-icepll", *argv])


def _run_icepll_argv():
    sys.exit(run_icepll(sys.argv[1:]))


def run_icebram(argv):
    return _run_wasm_app("icebram.wasm", ["yowasp-icebram", *argv])


def _run_icebram_argv():
    sys.exit(run_icebram(sys.argv[1:]))


def run_icemulti(argv):
    return _run_wasm_app("icemulti.wasm", ["yowasp-icemulti", *argv])


def _run_icemulti_argv():
    sys.exit(run_icemulti(sys.argv[1:]))


def run_icepack(argv):
    return _run_wasm_app("icepack.wasm", ["yowasp-icepack", *argv])


def _run_icepack_argv():
    sys.exit(run_icepack(sys.argv[1:]))


def run_iceunpack(argv):
    # same binary as icepack, operation distinguished with argv[0]
    return _run_wasm_app("icepack.wasm", ["yowasp-iceunpack", *argv])


def _run_iceunpack_argv():
    sys.exit(run_iceunpack(sys.argv[1:]))


def run_nextpnr_ice40(argv):
    return _run_wasm_app("nextpnr-ice40.wasm", ["yowasp-nextpnr-ice40", *argv])


def _run_nextpnr_ice40_argv():
    sys.exit(run_nextpnr_ice40(sys.argv[1:]))
