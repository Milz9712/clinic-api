from fastapi import FastAPI, HTTPException

app = FastAPI()

TREATMENTS = [
    {"id": 1, "name": "deep tissue", "price": 50},
    {"id": 2, "name": "massage", "price": 45}, 
    {"id": 3, "name": "sports recovery", "price": 65},
]

@app.get("/")
def home():
    return {"clinic": "Hainault Health Clinic", "status": "open"} 

@app.get("/treatments")
def treatments():
    return TREATMENTS

@app.get("/treatments/{treatment_id}")
def get_treatment(treatment_id: int): 
    for t in TREATMENTS: 
        if t["id"] == treatment_id:
            return t
    raise HTTPException(status_code=404, detail="Treatment not found")
