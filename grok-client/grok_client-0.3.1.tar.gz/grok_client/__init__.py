import pexpect
import logging
from threading import Thread
from os.path import expanduser, join, isfile
from tempfile import gettempdir
import signal
from subprocess import check_output
import platform
from enum import IntEnum
import yaml

LOG = logging.getLogger("Ngrok")


class NgrokException(Exception):
    """ something went wrong with ngrok"""


class NgrokStatus(IntEnum):
    LOADING = 0
    AUTHENTICATING = 10
    WAITING = 20
    RUNNING = 30
    FORWARDING = 40
    CONNECTED = 50
    CLOSED = 60
    FORBIDDEN = 70
    ERROR = 80
    EXITED = 90
    INSTALLING = 100
    NOT_LOADED = 110


class Ngrok(Thread):
    def __init__(self, authtoken=None, config=None,
                 port=22, proto="tcp", debug=True):
        super().__init__()
        self.status = NgrokStatus.NOT_LOADED
        self.debug = debug
        self.proto = proto
        if config is not None:
            config = expanduser(config)
        self.config = config
        if debug:
            LOG.setLevel(logging.DEBUG)
        else:
            LOG.setLevel(logging.INFO)
        self.running = False
        self.port = str(port)
        self.ngrok = None
        self._prev_output = ""

        self.maybe_install()

        self.handle_status_change(NgrokStatus.LOADING)

        self.authtoken = authtoken
        self.handle_status_change(NgrokStatus.WAITING)

        self.host = None
        self.connection_port = None

        self._initial_conf = None

    def backup_config(self):
        if self.config is None:
            self._initial_conf = {}
        else:
            with open(self.config, "r") as f:
                self._initial_conf = yaml.load(f, Loader=yaml.SafeLoader)

    def restore_config(self):
        if self.config is not None:
            with open(self.config, "w") as f:
                yaml.dump(self._initial_conf, f)

    def override_config(self):
        if self.config is not None:
            conf_path = self.config
            with open(self.config, "r") as f:
                conf = yaml.load(f, Loader=yaml.SafeLoader)
        else:
            conf_path = join(gettempdir(), "ngrok.yml")
            conf = {}

        conf["log"] = "stdout"
        if self.authtoken:
            conf["authtoken"] = self.authtoken
        with open(conf_path, "w") as f:
            yaml.dump(conf, f)

    def maybe_install(self):
        try:
            check_output(["ngrok", "-h"])
            installed = True
        except FileNotFoundError:
            installed = False

        if installed:
            return

        self.handle_status_change(NgrokStatus.INSTALLING)

        is_arm = "x86_64" not in platform.platform()
        # TODO download binaries
        if is_arm:
            print("install arm")
        else:
            print("install linux")
        raise NgrokException("ngrok not installed")

    def handle_status_change(self, status):
        LOG.debug("Status {current} -> {new} ".format(current=self.status,
                                                      new=status))
        self.status = status

    def handle_open(self, address):
        LOG.info("Connect at " + str(address))
        self.host, self.connection_port = address.split("//")[1].split(":")

    def handle_connected(self, addr):
        print("Connected", addr)

    def handle_closed(self):
        print("Closed")

    def handle_error(self, out):
        LOG.error(out)

        raise NgrokException(out)

    def launch(self) -> None:
        if not self.running:
            self.backup_config()
            self.override_config()

            self.running = True
            if self.config is not None:
                LOG.info("Starting ngrok from config " + self.config)
                if not isfile(self.config):
                    raise NgrokException("Config file does not exist")
                self.ngrok = pexpect.spawn('ngrok start -config {conf} '
                                           '--all'.format(conf=self.config))
            else:
                LOG.info("Starting ngrok {proto} {port}".format(
                    proto=self.proto, port=self.port))
                self.ngrok = pexpect.spawn('ngrok {proto} {port}'.format(
                    proto=self.proto, port=self.port))
            self.handle_status_change(NgrokStatus.RUNNING)
        else:
            LOG.error("Already running")
            raise NgrokException("Already running")

    def stop(self, ignore_exc=True) -> None:
        self.running = False
        self.restore_config()
        if self.ngrok is not None:
            self.ngrok.close()
            self.ngrok.kill(signal.SIGKILL)
            self.handle_status_change(NgrokStatus.EXITED)
            self.ngrok = None
        else:
            if not ignore_exc:
                LOG.error("Already stopped")
                raise NgrokException("Already stopped")

    def run(self):
        self.launch()
        while self.running:
            try:
                out = self.ngrok.readline().decode("utf-8")
                if out != self._prev_output:
                    out = out.strip()
                    if self.debug:
                        LOG.debug(out)
                    if "Your account " in out and " is limited to 1 simultaneous ngrok client session." in out:
                        self.handle_status_change(NgrokStatus.FORBIDDEN)
                        self.handle_error(out)
                    elif "ngrok does not support a dynamic, color terminal " \
                         "UI on solaris." in out:
                        self.handle_status_change(NgrokStatus.ERROR)
                        self.handle_error(out)
                    elif "obj=tunnels.session err=" in out:
                        err = out.split("err=\"")[1].split("\"")[0] \
                            .replace("\\n", "\n").replace("\\r", "")
                        self.handle_status_change(NgrokStatus.ERROR)
                        self.handle_error(err)
                    elif "ERROR: " in out:
                        self.handle_status_change(NgrokStatus.ERROR)
                        self.handle_error(out)
                    # requires logging to stdout in .conf
                    elif " msg=\"started tunnel\" obj=tunnels " in out:
                        addrr = out.split("url=")[1]
                        self.handle_status_change(NgrokStatus.FORWARDING)
                        self.handle_open(addrr)
                    elif " msg=\"join connections\" obj=join" in out:
                        self.handle_status_change(NgrokStatus.CONNECTED)
                        self.handle_connected(out.split("r=")[-1])
                    elif "msg=\"session closing\"" in out:
                        self.handle_status_change(NgrokStatus.CLOSED)
                        self.handle_closed()

                    self._prev_output = out
            except pexpect.exceptions.EOF:
                # ngrok exited
                self.running = False
            except pexpect.exceptions.TIMEOUT:
                # nothing happened for a while
                pass
            except NgrokException:
                self.running = False
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                LOG.exception(e)
                self.handle_status_change(NgrokStatus.ERROR)
                self.handle_error(str(e))
                raise
        self.quit()

    def quit(self):
        LOG.info("Exiting")
        self.stop(True)
        self.restore_config()
        print("restored")
