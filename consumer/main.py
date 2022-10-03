import asyncio
from typing import Dict, List

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from aiokafka import AIOKafkaConsumer, TopicPartition, ConsumerRecord
import logging

from .kafka_client import consume

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
@app.get("/whoami")
def whoami():
    return JSONResponse(content={"name": "consumer"}, status_code=200)


@app.get("/health")
def health():
    return JSONResponse(
        content={"status": "ok"},
        status_code=200,
    )


@app.on_event("startup")
async def startup_event():
    logger.info("startup event")
    logger.info('start consuming messages')
    asyncio.get_running_loop().run_until_complete(await consume())
