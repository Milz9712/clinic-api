from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()

TREATMENTS = [
    {"id": 1, "name": "deep tissue", "price": 50},
    {"id": 2, "name": "massage", "price": 45},
    {"id": 3, "name": "sports recovery", "price": 65},
]


class treatment(BaseModel):
    name: str
    price: int


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


@app.post("/treatments")
def add_treatment(treatment: treatment):
    new = {"id": len(TREATMENTS) + 1, "name": treatment.name, "price": treatment.price}
    TREATMENTS.append(new)
    return new


@app.delete("/treatments/{treatment_id}")
def delete_treatment(treatment_id: int):
    for t in TREATMENTS:
        if t["id"] == treatment_id:
            TREATMENTS.remove(t)
            return {"deleted": t}
    raise HTTPException(status_code=404, detail="Treatment not found")
