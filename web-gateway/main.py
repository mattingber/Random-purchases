"""Web Gateway"""
import logging
import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from aiokafka import AIOKafkaProducer

from config import settings
from routers import router as userbuys_router

app = FastAPI()
loop = asyncio.get_event_loop()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_db_client():
    '''Initialize Kafka producer on FASTApi startup'''
    try:
        print("INFO:     trying to connect to kafka...")
        app.producer = AIOKafkaProducer(
            bootstrap_servers= settings.KAFKA_URL,
        )
        await app.producer.start()
        print("INFO:     kafka connection succeded!")
    except:
        print("error in connection to kafka")
        await app.producer.stop()
        raise HTTPException(status_code=500, detail="Failed to initialize the application")


@app.on_event("shutdown")
async def shutdown_db_client():
    '''Stops Kafka producer on FASTApi shutdown'''
    await app.producer.stop()

app.include_router(userbuys_router, tags=["userbuys"], prefix="/userbuys")


def main():
    '''Runs FASTApi'''
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )

if __name__ == "__main__":
    main()
