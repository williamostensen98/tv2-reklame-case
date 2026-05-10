# FastAPI Kafka TV2 Caseoppgave

A lightweight HTTP service that receives arbitrary JSON data and forwards it persistently to a Kafka topic.

## Project Structure

```
project/
├── main.py
├── producer.py
├── requirements.txt
├── improvements.md
├── journal-md
├── docker-compose.yml
└── README.md
```

## Requirements

- Python 3.11+
- Docker and Docker Compose

## Setup

### 1. Clone the repository

```bash
git clone git@github.com:williamostensen98/tv2-reklame-case.git
cd tv2-reklame-case
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Starting Kafka

Kafka runs through Docker Compose. Start it with:

```bash
docker compose up -d
```

This starts Kafka in the background with the following ports:

| Port | Usage |
|------|-------|
| `9092` | Internal Docker network (container-to-container) |
| `9093` | Internal KRaft controller (do not use) |
| `9094` | External access from your host machine |

To check that Kafka is running and healthy:

```bash
docker compose ps
```

To stop Kafka:

```bash
docker compose down
```

To stop Kafka and remove all stored data:

```bash
docker compose down -v
```

## Running the FastAPI Server

With Kafka running, start the FastAPI development server:

```bash
fastapi dev 
```

The server will start on `http://localhost:8000` with auto-reload enabled.

> **Note:** When running locally, the app connects to Kafka via `localhost:9094` (the external port). The `kafka:9092` address is only used when the app itself runs inside Docker.

### Swagger UI

FastAPI auto-generates interactive API docs available at:

```
http://localhost:8000/docs
```

## Testing with curl

### Send a valid JSON payload

```bash
curl -X POST http://localhost:8000/userdata \
  -H "Content-Type: application/json" \
  -d '{"id": "1", "test": "test"}'
```

Expected response:

```json
"200 OK"
```

### Test with invalid JSON (should return 400)

```bash
curl -X POST http://localhost:8000/userdata \
  -H "Content-Type: application/json" \
  -d 'not valid json' 
```
Expected response:

```json
"Status 400 - Invalid JSON"
```


### Verify the message reached Kafka

```bash
docker exec -it kafka kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic user-data --from-beginning
```
