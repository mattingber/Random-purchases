"""Represents the routes the gateway exposes"""
import json
import requests

from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import UserBuyModel
from config import settings

router = APIRouter()


@router.post("/", response_description="Add new user buy")
async def create_userbuy(request: Request, userbuy: UserBuyModel = Body(...)):
    '''Formats and validates a user-buy data object and producing it to kafka'''
    userbuy = json.dumps(jsonable_encoder(userbuy)).encode()
    await request.app.producer.send_and_wait("mytopic", userbuy)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"successfully added to topic": "mytopic"})


@router.get("/{userid}", response_description="List all userbuys by userID")
async def list_userbuys(userid: str, request: Request):
    '''Gets user-buys by USERID of user-buy'''
    url = f"{settings.API_URL}/userbuys/{userid}"
    pourchases = requests.get(url)
    return JSONResponse( status_code=status.HTTP_201_CREATED, content = pourchases.json())
