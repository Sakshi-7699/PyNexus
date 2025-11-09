from typing import Optional, List
from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import logging
import uvicorn
from datetime import datetime

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title = "PyNexus API",
    description = "API for managing PyNexus resources",
    version = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)