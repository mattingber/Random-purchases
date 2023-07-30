"""Holds Utility functions for the code"""
import json

from fastapi.encoders import jsonable_encoder

from models import UserBuyModel

async def consume(app):
    ''' asynchronous consuming of the app's kafka consumer'''
    try:
        async for msg in app.consumer:
            try:
                decoded_msg = msg.value.decode('utf8')
                data = json.loads(decoded_msg)
                data_modeled = UserBuyModel(**data)
                data_modeled_json = jsonable_encoder(data_modeled)
                mongod = await app.mongodb["userbuys"].insert_one(data_modeled_json)
                print(mongod.inserted_id)
            except Exception as e:
                print(f"Error while proccessing data object to mongo: {e}")
                continue

    finally:
        await app.consumer.stop()
