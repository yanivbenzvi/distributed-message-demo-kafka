import asyncio

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging

from kafka_client import KafkaProducer

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/health")
def health():
    return JSONResponse(
        content={"status": "ok"},
        status_code=200,
    )


@app.get("/whoami")
@app.get("/")
def whoami():
    response = jsonable_encoder({"name": "producer"})
    return JSONResponse(content=response)


@app.get("/produce")
async def produce():
    producer = KafkaProducer(
        bootstrap_servers=["message-service-kafka-cluster:9092"],
        topic="test-topic",
        loop=asyncio.get_running_loop()
    )

    if producer is None:
        return {"status": "error", "message": "producer not initialized"}

    await producer.send_message("Hello World")
    response = jsonable_encoder({"status": "ok"})
    return JSONResponse(content=response)


@app.on_event("startup")
async def startup_event():
    producer = KafkaProducer(
        bootstrap_servers=["message-service-kafka-cluster:9092"],
        topic="test-topic",
        loop=asyncio.get_running_loop()
    )
    logger.info("startup event")

    # await producer.test_connection()


@app.on_event("shutdown")
async def shutdown_event():
    print("shutdown event")
