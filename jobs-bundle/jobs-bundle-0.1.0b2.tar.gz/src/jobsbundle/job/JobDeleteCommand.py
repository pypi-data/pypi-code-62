from argparse import ArgumentParser, Namespace
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from databricks_api.databricks import DatabricksAPI

class JobDeleteCommand(ConsoleCommand):

    def __init__(
        self,
        logger: Logger,
        dbxApi: DatabricksAPI,
    ):
        self.__logger = logger
        self.__dbxApi = dbxApi

    def getCommand(self) -> str:
        return 'databricks:job:delete'

    def getDescription(self):
        return 'Deletes a Databricks job'

    def configure(self, argumentParser: ArgumentParser):
        argumentParser.add_argument(dest='jobId', help='Job ID')

    def run(self, inputArgs: Namespace):
        self.__logger.info(f'Deleting job {inputArgs.jobId}')

        self.__dbxApi.jobs.delete_job(inputArgs.jobId)

        self.__logger.info(f'Job successfully delete')
