from abc import abstractmethod
from logging import info


class BaseSource(object):

    @abstractmethod
    def read(self, source_ids=None):
        """
        Read from the source and get the data frame
        :param: source_ids list of ids to help fetch the data
        :return: data frame with the time series
        """


class BaseIngress(object):

    @abstractmethod
    def ingress(self, input_to_process):
        """
        Business logic for ingress
        :param input_to_process: the input from the source
        :return: message to be transformed
        """


class BaseTransformer(object):

    @abstractmethod
    def transform(self, input_to_transform):
        """
        Business logic for ingress
        :param input_to_transform: the input from the source for transformation
        :return: transformed message
        """


class BaseEgress(object):

    @abstractmethod
    def egress(self, transform_output):
        """
        Logic to egress it to downstream
        :param transform_output: the output of transformation
        """


class BaseFlow(object):

    def __init__(self, ingress, transformer, egress):
        self._ingress = ingress
        self._transformer = transformer
        self._egress = egress

    def process(self, tasks=None):
        """
        Processes the message by flowing it through the 3 phases
        :param tasks: the identifiers to be processed during the flow
        """
        info(f"{self._ingress}: Starting Ingress stage")
        self._ingress.ingress(tasks)
        info(f"{self._transformer}: Starting Transform stage")
        transformed_output = self._transformer.transform(tasks)
        info(f"{self._egress}: Starting egress stage")
        self._egress.egress(transformed_output)
