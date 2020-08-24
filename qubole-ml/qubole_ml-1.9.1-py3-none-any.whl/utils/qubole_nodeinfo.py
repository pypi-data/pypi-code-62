from subprocess import Popen, PIPE


class NodeInfo(object):
    """
    Utility class to call qubole nodinfo script and fetch values
    """
    QUBOLE_BASH_LIB_FILE = "/usr/lib/hustler/bin/qubole-bash-lib.sh"

    @classmethod
    def _execute(cls, command):
        proc = Popen(["source {} && {}".format(
                  cls.QUBOLE_BASH_LIB_FILE, command)],
                stdout=PIPE,
                stderr=PIPE,
                shell=True,
                executable='/bin/bash')

        return proc.stdout.readline().decode('utf-8').rstrip("\n")

    @classmethod
    def get_info(cls, key):
        """
        Return value from nodeinfo
        :return: :py:class:`string`
        """
        return cls._execute("nodeinfo {}".format(key))

    @classmethod
    def get_feature(cls, key):
        """
        Returns a feature value from nodeinfo
        :return: :py:class:`bool`
        """
        return cls._execute("nodeinfo_feature {}".format(key)) == "true"
