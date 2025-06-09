import os
import logging
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import artist

app = FastAPI(
    title="IDK",
    version="1.0.0",
)

origins =[
    "http://localhost:8000",
    "https://spark.ychan.me",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(artist.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}