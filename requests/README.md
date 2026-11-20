# Test requests

Request bodies kept in files, so curl commands stay short. `-d @file` tells curl to send the file's contents as the body.

All data here is made up. Never put real client names or phone numbers in this folder: it's committed to GitHub.

Run these from the project root while the server is running.

## Bookings

| File | What it tests | Expected |
|---|---|---|
| `booking_ok.json` | valid booking, treatment 2 | 200 + the new booking |
| `booking_bad_treatment.json` | treatment 99 doesn't exist | 404 |
| `booking_bad_date.json` | `"next tuesday"` isn't a datetime | 422, `loc: ["body", "starts_at"]` |

```
curl -X POST localhost:8000/bookings -H "Content-Type: application/json" -d @requests/booking_ok.json
curl -X POST localhost:8000/bookings -H "Content-Type: application/json" -d @requests/booking_bad_treatment.json
curl -X POST localhost:8000/bookings -H "Content-Type: application/json" -d @requests/booking_bad_date.json
curl localhost:8000/bookings
```

## Treatments

```
curl -X POST localhost:8000/treatments -H "Content-Type: application/json" -d @requests/treatment_ok.json
curl localhost:8000/treatments
```

## Shortcut

Save typing the header every time:

```
H="Content-Type: application/json"
curl -X POST localhost:8000/bookings -H "$H" -d @requests/booking_ok.json
```

`H` lasts until you close the Shell tab.
