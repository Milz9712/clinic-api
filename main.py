from psycopg.errors import ForeignKeyViolation
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from datetime import datetime

from pydantic import BaseModel

import logging

import os
import psycopg

DATABASE_URL = os.environ["DATABASE_URL"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    with psycopg.connect(DATABASE_URL) as conn:
        with open("schema.sql") as f:
            conn.execute(f.read())
    yield


app = FastAPI(lifespan=lifespan)


class Treatment(BaseModel):
    name: str
    price: int


class Booking(BaseModel):
    client_name: str
    client_phone: str
    treatment_id: int
    starts_at: datetime


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
    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "INSERT INTO treatments (name, price) VALUES (%s, %s) RETURNING id, name, price",
            (treatment.name, treatment.price),
        ).fetchone()
        if row is None:
            logger.error("Treatment insert returned no row")
            raise HTTPException(status_code=500, detail="Failed to create treatment")
    return {"id": row[0], "name": row[1], "price": row[2]}


@app.delete("/treatments/{treatment_id}")
def delete_treatment(treatment_id: int):
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            row = conn.execute(
                "DELETE FROM treatments WHERE id = %s RETURNING id, name, price",
                (treatment_id,),
            ).fetchone()
    except ForeignKeyViolation:
        logger.warning("Treatment %s has bookings, not deleted", treatment_id)
        raise HTTPException(
            status_code=409, detail="Treatment has bookings and can't be deleted"
        )
    if row is None:
        logger.warning("Treatment not found: %s", treatment_id)
        raise HTTPException(status_code=404, detail="Treatment not found")
    return {"deleted": {"id": row[0], "name": row[1], "price": row[2]}}


@app.post("/bookings")
def add_booking(booking: Booking):
    logger.info("Creating booking for the treatment %s", booking.treatment_id)
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            row = conn.execute(
                "INSERT INTO bookings (client_name, client_phone, treatment_id, starts_at) "
                "VALUES (%s, %s, %s, %s) RETURNING id, client_name, client_phone, treatment_id, starts_at",
                (
                    booking.client_name,
                    booking.client_phone,
                    booking.treatment_id,
                    booking.starts_at,
                ),
            ).fetchone()
    except ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="Treatment not found")
    if row is None:
        raise HTTPException(status_code=500, detail="Failed to create booking")
    return {
        "id": row[0],
        "client_name": row[1],
        "client_phone": row[2],
        "treatment_id": row[3],
        "starts_at": row[4],
    }


@app.get("/bookings")
def list_bookings():
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            "SELECT id, client_name, client_phone, treatment_id, starts_at FROM bookings ORDER BY starts_at"
        ).fetchall()
    return [
        {"id": r[0], "client_name": r[1], "client_phone": r[2], 
         "treatment_id": r[3], "starts_at": r[4]}
        for r in rows
    ]

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        row = conn.execute(
            "DELETE FROM bookings WHERE id = %s RETURNING id", 
            (booking_id,), 
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"deleted": {"id": row[0]}}