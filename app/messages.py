import aiokafka


class KafkaPublisher:
    def __init__(self) -> None:
        aiokafka.AIOKafkaProducer()