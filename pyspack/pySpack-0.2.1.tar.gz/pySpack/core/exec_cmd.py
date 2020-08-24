import subprocess
from subprocess import PIPE
from sys import version_info
from typing import List


def exec_cmd(program: str, arguments: List) -> subprocess.CompletedProcess:
    if version_info.minor > 6:
        return subprocess.run([program, *arguments], capture_output=True)
    return subprocess.run([program, *arguments], stdout=PIPE, stderr=PIPE)
