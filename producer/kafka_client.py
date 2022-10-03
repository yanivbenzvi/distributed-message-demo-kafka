# Kafka client class for producer
import asyncio
import logging
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError


class KafkaProducer:
    def __init__(self, topic: str, bootstrap_servers: list | str, loop: asyncio.AbstractEventLoop):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.loop = loop

    async def test_connection(self):
        producer = AIOKafkaProducer(
            loop=self.loop,
            bootstrap_servers=self.bootstrap_servers,
        )

        try:
            await asyncio.get_running_loop().run_until_complete(producer.start())
            await asyncio.get_running_loop().run_until_complete(producer.stop())
            return True

        except KafkaError as e:
            logging.error(e)
            return False

    async def send_message(self, message: str):
        producer = AIOKafkaProducer(
            loop=self.loop,
            bootstrap_servers=self.bootstrap_servers,
        )

        await producer.start()
        try:
            await producer.send_and_wait(self.topic, message.encode("utf-8"))
        except KafkaError as e:
            logging.error(e)
        finally:
            await producer.stop()
