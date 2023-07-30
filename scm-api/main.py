"""User-buys API """
import json
import logging
import asyncio
import uvicorn

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from aiokafka import AIOKafkaConsumer


from config import settings
from routers import router as userbuys_router
from models import UserBuyModel
from utils import consume


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup_db_client():
    '''Initiating mongodb and Kafka consumer connection on FASTApi startup'''
    print("INFO:     trying to connect to mongo...")
    try:
        #Initiating Mongo connection
        app.mongodb_client = AsyncIOMotorClient(settings.DB_URL, serverSelectionTimeoutMS=5000)
        app.mongodb = app.mongodb_client[settings.DB_NAME]
        await app.mongodb.command("ping")
        print("INFO:     mongo connection succeded!")

        # Initiating a kafka consumer connection
        app.consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_HOST,
    )
        await app.consumer.start()
        print("kafka connection succeded")

        # creates an asynchronous task for the consumer
        asyncio.create_task(consume(app))

    except:
        print("error in connection to db")
        raise HTTPException(status_code=500, detail="Failed to initialize the application")

@app.on_event("shutdown")
async def shutdown_db_client():
    '''closing mongodb connection on FASTApi shutdown'''
    try:
        app.mongodb_client.close()
    except RuntimeError as e:
        print(e)

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
