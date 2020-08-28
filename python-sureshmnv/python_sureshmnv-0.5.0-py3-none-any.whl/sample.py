from logging_sureshmnv import *
from subprocess_sureshmnv import *

print('name of module in sample global is', __name__)
logger = logging_mnv_set(logName=__name__, logLevel=logging.DEBUG)
#logger = logging_mnv_get(logName=__name__)
#logger = logging_mnv_get()

if __name__ == "__main__":
    print('name of module in sample main is', __name__)
    logger = logging_mnv_get(logName=__name__)
    #logger = logging_mnv_set(logLevel=logging.DEBUG)
    #out_lines, err_lines = subprocess_cmd('date2')

    out_lines, err_lines = subprocess_cmd('date')
    out_lines, err_lines = subprocess_cmd('whoami')
