from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

import httpx
import uvicorn
import asyncio
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="PyNexus API",
    description="API for managing PyNexus resources",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_ENDPOINTS = {
    "weather": "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true",
    "crypto": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum",
}

class APIOptions(str, Enum): 
    WEATHER = "weather"
    CRYPTO = "crypto"
class SelectOptions(BaseModel):
    options: list[APIOptions]  # List of API names from the dropdown

async def fetch_data(client: httpx.AsyncClient, name: str, url: str):
    try:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return {name: response.json()}
    except Exception as e:
        return {name: {"error": str(e)}}

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the PyNexus API"}    

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "service": "PyNexus API",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/all-data", tags=["Aggregated Data"])
async def get_aggregated_data():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_data(client, name, url) for name, url in API_ENDPOINTS.items()]
        results = await asyncio.gather(*tasks)
    return results

@app.post("/selective-data", tags=["Aggregated Data"])
async def get_selective_aggregated_data(selection: SelectOptions):
    selected_apis = {name: API_ENDPOINTS[name] for name in selection.options if name in API_ENDPOINTS}
    async with httpx.AsyncClient() as client:
        tasks = [fetch_data(client, name, url) for name, url in selected_apis.items()]
        results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
