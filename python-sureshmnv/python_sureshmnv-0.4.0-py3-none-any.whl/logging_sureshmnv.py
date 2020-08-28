#!/usr/bin/env python3
import logging

def logging_mnv_get(**kwargs):
    if 'logName' in kwargs.keys():
      logger = logging.getLogger(kwargs['logName'])
    else:
      logger = logging.getLogger(__name__)

    return logger

def logging_mnv_set(**kwargs):
    if 'logName' in kwargs.keys():
      logger = logging.getLogger(kwargs['logName'])
    else:
      logger = logging.getLogger(__name__)

    if 'logLevel' in kwargs.keys():
      logger.setLevel(kwargs['logLevel'])

    if 'logFile' in kwargs.keys():
      file_handler = logging.FileHandler(kwargs['logFile'])
    else:
      file_handler = logging.FileHandler('logfile.log')

    if 'logFormatter' in kwargs.keys():
      formatter    = logging.Formatter(kwargs['logFormatter'])
    else:
      formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
  logger = logging_mnv_get(logName='testlog', logLevel=logging.ERROR, logFile='testlog.log',
      logFormatter='%(asctime)s : %(funcName)s : %(levelname)s : %(name)s : %(message)s')

  logger.critical('A Fatal error')

  logger = logging_mnv_get(logLevel=logging.ERROR,
      logFormatter='%(asctime)s : %(funcName)s : %(levelname)s : %(name)s : %(message)s')

  logger.critical('A Fatal error without logFile')

  logger = logging_mnv_get(logLevel=logging.ERROR, logFile='testlog.log',
      logFormatter='%(asctime)s : %(funcName)s : %(levelname)s : %(name)s : %(message)s')

  logger.critical('A Fatal error without logname')

  logger = logging_mnv_get(logLevel=logging.ERROR, logFile='testlog.log')

  logger.critical('A Fatal error without logFormatter')
