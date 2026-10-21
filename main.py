from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"clinic": "Hainault Health Clinic", "status": "open"} 

@app.get("/treatments")
def treatments():
    return [
      {"name": "deep tissue", "price": 50},
      {"name": "massage", "price": 45},
      {"name": "sports recovery", "price": 65},
    ]
  