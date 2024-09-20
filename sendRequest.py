from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from contextlib import asynccontextmanager

windmill_status = {"signal": "on"}  # Start with the windmill running

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic to stop windmill when app starts
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/api/windmill/stop")
        print(f"POST /api/windmill/stop response: {response.json()}")
    yield  # Application runs here
    # Add any shutdown logic if necessary

app = FastAPI(lifespan=lifespan)

# CORS setup to allow React frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/windmill/status")
async def get_windmill_status():
    return windmill_status

@app.post("/api/windmill/stop")
async def stop_windmill():
    print("Windmill stop request received")  # Log when the stop request is made
    windmill_status["signal"] = "off"
    return {"message": "Windmill stopped"}
