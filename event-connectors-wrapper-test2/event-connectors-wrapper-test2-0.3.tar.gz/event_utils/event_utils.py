from kafka_utils.kafka_utils import KafkaConsumer, KafkaProducer


class EventConsumer:
    """
    Class to create a event consumer
    """
    consumer_engines = {
        'kafka': KafkaConsumer
    }

    def __init__(self, engine, config):
        self.consumer = self.consumer_engines[engine](**config)

    def create_consumer(self):
        """
        Given the configuration returns a configured consumer for the given engine
        :return: Consumer for a given engine
        """
        return self.consumer


class EventProducer:
    """
    Class to create a event producer
    """
    producer_engines = {
        'kafka': KafkaProducer
    }

    def __init__(self, engine, config):
        self.producer = self.producer_engines[engine](**config)

    def create_producer(self):
        """
        Given the configuration returns a configured producer for the given engine
        :return: Consumer for a given engine
        """
        return self.producer