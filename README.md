# clinic-api

This API is for Hainault Health clinic where the API talks to my server by sending a request to an address, get data back. the clinic api lets someone get the treatment list, look up one treatment or add a new one. 

## How to run it

```
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Run the tests

```
pytest
```

Expected: 7 passed

What the tests cover:
- GET /treatments returns 200 (list works)
- GET /treatments/99 returns 404 (treatment doesn't exist)
- GET /treatments/abc returns 422 (id isn't a number)
- POST /treatments with a name and price returns 200, and the response contains the name it sent (cupping)
- POST /treatments with a name only returns 422, wrong input as price is missing
- DELETE /treatments/2 returns 200, the second DELETE returns 404 because treatment 2 no longer exists. 
- GET /treatments/99 returns a 404, and the app logs a warning, which the test checks with caplog.

## Endpoints 

| Method | Path | What it does |
|--------|------|--------------|
| GET | / | Health check. Returns the clinic name and status |
| GET | /treatments | Returns all treatments |
| GET | /treatments/{id} | Returns one treatment by ID. 404 if not found, 422 if the ID isn't a number |
| POST | /treatments | Adds a new treatment. Needs name and price, 422 if either is missing. | 
| DELETE | /treatments/{id} | Removes a treatment by ID. 404 if not found |

## Example

```
curl localhost:8000/treatments 
[{"id":1,"name":"deep tissue","price":50},{"id":2,"name":"massage","price":45},{"id":3,"name":"sports recovery","price":65}]
```

## What I'm building next

- Store data in a Postgres database instead of memory
- Deploy it online

## Logging

When a treatment is created, the app logs: an INFO line with its name for example "Creating treatment: cupping". 
When a treatment isn't found (GET or DELETE), the app logs a WARNING with the id, for example "Treatment not found: 99"
These lines can be seen on the server console where the uvicorn is running.

 