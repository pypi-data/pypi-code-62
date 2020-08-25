from confluent_kafka import Consumer, Producer


class KafkaConfig:
    """
    Class with init function doing basic configuration for kafka service
    """
    def __init__(self, CLOUDKARAFKA_BROKERS, CLOUDKARAFKA_PASSWORD, CLOUDKARAFKA_USERNAME):
        self.username = CLOUDKARAFKA_USERNAME
        self.conf = {
            'bootstrap.servers': CLOUDKARAFKA_BROKERS,
            'group.id': "%s-consumer" % (CLOUDKARAFKA_USERNAME),
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'latest'},
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': CLOUDKARAFKA_USERNAME,
            'sasl.password': CLOUDKARAFKA_PASSWORD,
            'auto.offset.reset': 'latest',
            'partition.assignment.strategy': 'roundrobin'
        }


class KafkaConsumer(KafkaConfig):
    """
    Class to create a kafka consumer
    """
    def __init__(self, CLOUDKARAFKA_BROKERS, CLOUDKARAFKA_PASSWORD, CLOUDKARAFKA_USERNAME):
        super().__init__(CLOUDKARAFKA_BROKERS, CLOUDKARAFKA_PASSWORD, CLOUDKARAFKA_USERNAME)
        self.kafka_consumer = Consumer(**self.conf)

    def assign_topic(self, topics):
        """
        Assign a topic for the kafka_consumer
        :param topics: Name of the topic
        """
        final_topics = []
        for item in topics:
            final_topics.append(self.username + '-' + item)
        self.kafka_consumer.subscribe(final_topics)

    def get_message(self, timeout=1):
        return self.kafka_consumer.poll(timeout=timeout)


class KafkaProducer(KafkaConfig):
    """
    Class to create a kafka producer
    """
    def __init__(self, CLOUDKARAFKA_BROKERS, CLOUDKARAFKA_PASSWORD, CLOUDKARAFKA_USERNAME):
        super().__init__(CLOUDKARAFKA_BROKERS, CLOUDKARAFKA_PASSWORD, CLOUDKARAFKA_USERNAME)
        self.kafka_producer = Producer(**self.conf)

    def send_message(self, topic: str, message: str, headers: dict = None):
        """
        Sends a message to for given topic to the kafka service
        :param message: String with the message to be send to the kafka service. Ie. 'some message'
        :param topic: String with the topic of the message. Ie. 'introduction-topic'
        :param headers: Dict with additional headers for the message. Ie. {'header1': 'value1', 'header2': 'value2'}
        """
        msg_headers = []
        if headers is not None:
            for header in headers.keys():
                msg_headers.append((
                    header,
                    bytes(headers[header], encoding='utf8')
                ))
        try:
            topic = self.username + '-' + topic
            self.kafka_producer.produce(topic, message, headers=msg_headers)
            self.kafka_producer.flush()
        except BufferError as e:
            raise