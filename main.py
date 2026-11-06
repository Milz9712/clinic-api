from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

import logging

import os
import psycopg

DATABASE_URL = os.environ["DATABASE_URL"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

TREATMENTS = [
    {"id": 1, "name": "deep tissue", "price": 50},
    {"id": 2, "name": "massage", "price": 45},
    {"id": 3, "name": "sports recovery", "price": 65},
]


class Treatment(BaseModel):
    name: str
    price: int


@app.get("/")
def home():
    return {"clinic": "Hainault Health Clinic", "status": "open"}


@app.get("/treatments")
def treatments():
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            "SELECT id, name, price FROM treatments ORDER BY id"
        ).fetchall()
    return [{"id": r[0], "name": r[1], "price": r[2]} for r in rows]


@app.get("/treatments/{treatment_id}")
def get_treatment(treatment_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "SELECT id, name, price FROM treatments WHERE id = %s", (treatment_id,)
        ).fetchone()
    if row is None:
        logger.warning("Treatment not found: %s", treatment_id)
        raise HTTPException(status_code=404, detail="Treatment not found")
    return {"id": row[0], "name": row[1], "price": row[2]}


@app.post("/treatments")
def add_treatment(treatment: Treatment):
    logger.info("Creating treatment: %s", treatment.name)
    new = {"id": len(TREATMENTS) + 1, "name": treatment.name, "price": treatment.price}
    TREATMENTS.append(new)
    return new


@app.delete("/treatments/{treatment_id}")
def delete_treatment(treatment_id: int):
    for t in TREATMENTS:
        if t["id"] == treatment_id:
            TREATMENTS.remove(t)
            return {"deleted": t}
    logger.warning("Treatment not found: %s", treatment_id)
    raise HTTPException(status_code=404, detail="Treatment not found")
