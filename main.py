import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from confluent_kafka import Producer


producer_config = {'bootstrap.servers': 'localhost:9094'}

producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer
    producer = Producer(producer_config)
    yield
    producer.flush() # Ensure all messages are sent before shutdown

app = FastAPI(lifespan=lifespan)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.value().decode('utf-8')}")

@app.post("/userdata")
async def process_data_to_kafka(request: Request):

    try:
        data = await request.json()

    except Exception:
        raise HTTPException(status_code=400, detail=f"Status 400 - Invalid JSON")

    try:
        producer.produce(
            topic="user-data",
            value=json.dumps(data).encode("utf-8"),
            callback=delivery_report
        )
        producer.flush()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return JSONResponse(status_code=200, content="200 OK")
