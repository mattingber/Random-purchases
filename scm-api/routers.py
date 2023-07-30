"""Represents the routes the gateway exposes"""
from fastapi import APIRouter, Request


router = APIRouter()

@router.get("/{userid}", response_description="List all buys of user")
async def list_userbuys(userid: str, request: Request):
    '''Get all user-buys by USERID field'''
    userbuys = []
    for doc in await request.app.mongodb["userbuys"].find({"userid": userid}).to_list(length=100):
        print(doc)
        userbuys.append(doc)
    return userbuys
