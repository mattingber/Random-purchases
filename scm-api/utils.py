"""Holds Utility functions for the code"""
import json
import random

from fastapi.encoders import jsonable_encoder

from models import UserBuyModel

async def consume(app):
    ''' asynchronous consuming of the app's kafka consumer'''
    try:
        async for msg in app.consumer:
            try:
                decoded_msg = msg.value.decode('utf8')
                data = json.loads(decoded_msg)
                data["item"] = get_random_item()
                data_modeled = UserBuyModel(**data)
                data_modeled_json = jsonable_encoder(data_modeled)
                mongod = await app.mongodb["userbuys"].insert_one(data_modeled_json)
                print(mongod.inserted_id)
            except Exception as e:
                print(f"Error while proccessing data object to mongo: {e}")
                continue

    finally:
        await app.consumer.stop()


def get_random_item():
    """get random item of of an ENUM"""
    store_items = [
        "Pet Rock",
        "Disco Ball",
        "Inflatable Sword",
        "Magic 8 Ball",
        "Hoola Hoop",
        "Magic Ring",
        "Beans",
        "Cowboy Hat",
        "Stick Horse",
        "Fake Beard"
    ]

    return random.choice(store_items)