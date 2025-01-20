import aiokafka


class KafkaPublisher(aiokafka.AIOKafkaProducer):
    __topic = "applications"

    async def publish_message(self, message):
        await self.send(self.__topic, message)
