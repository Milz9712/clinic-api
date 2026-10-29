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

- More tests (POST and DELETE)
- Store data in a Postgres database instead of memory
- Deploy it online
