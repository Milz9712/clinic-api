CREATE TABLE IF NOT EXISTS treatments (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price INTEGER NOT NULL 
);

CREATE TABLE IF NOT EXISTS bookings (
  id SERIAL PRIMARY KEY,
  client_name TEXT NOT NULL,
  client_phone TEXT NOT NULL, 
  treatment_id INTEGER NOT NULL REFERENCES treatments(id), 
  starts_at TIMESTAMPTZ NOT NULL 
);