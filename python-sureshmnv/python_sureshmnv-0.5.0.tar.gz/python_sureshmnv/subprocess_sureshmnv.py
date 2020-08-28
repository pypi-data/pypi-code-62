#!/usr/bin/env python3
import subprocess
from python_sureshmnv.logging_sureshmnv import *
#from logging_sureshmnv import *

print('name of module in subproces global is', __name__)
logger = logging_mnv_set(logName=__name__, logLevel=logging.DEBUG)
"""
logger = logging_mnv_set(logName=__name__, logName='testlog', logLevel=logging.ERROR,
        logFile='testlog.log',
        logFormatter='%(asctime)s : %(funcName)s : %(levelname)s : %(name)s : %(message)s')
"""
#logger = logging_mnv_get(logName=__name__)

def subprocess_cmd(bash_cmd):
    print('name of module in subproces func is', __name__)
    logger = logging_mnv_get(logName=__name__)

    logger.info(bash_cmd)

    try:
        output = subprocess.check_output(bash_cmd, stderr=subprocess.STDOUT,
                shell=True, timeout=3, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        logger.exception("Status : FAIL", exc.returncode, exc.output)
        return "", exc.output
    else:
        logger.debug("Output: \n{}\n".format(output))
        return output, ""

    """
    proc = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, shell=True)
    #proc = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, stderr=devnull, shell=True)
    (output, err) = proc.communicate()

    err_lines = ''
    print(err)
    if err != None and len(err) > 1:
        err_lines = str(err, 'utf-8').split('\n')
        if (len(err_lines) > 1):
            for line in error_lines:
                logger.error(line)

    out_lines = str(output, 'utf-8').split('\n')
    #out_lines = str(output).split('\n')

    if (len(out_lines) > 1):
        for line in out_lines:
            logger.debug(line)

    """

if __name__ == "__main__":
    logger = logging_mnv_set(logName=__name__)
    #out_lines, err_lines = subprocess_cmd('date2')

    out_lines, err_lines = subprocess_cmd('date')
    out_lines, err_lines = subprocess_cmd('whoami')

    logger.info("Output: \n{}\n".format(out_lines))
