# Annalakshmi Data Management System

Internal data management system for **Oota.app**, built for Thorsignia. Enables the Operations Team to store, search, filter, update, and archive information about Annalakshmis (home-cooked meal providers).

> **Status:** Backend complete (CRUD, validation, pagination, error handling, tests). Frontend in progress.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Validation | Pydantic v2 |
| Database | SQLite |
| Testing | pytest + httpx (FastAPI TestClient) |
| Frontend (planned) | Bootstrap 5, vanilla JS, Jinja2 |

---

## Folder Structure

```
annalakshmi-dms/
├── app/
│   ├── main.py              # FastAPI app entrypoint, exception handlers
│   ├── database.py          # DB engine/session setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas + validation rules
│   ├── crud.py               # DB operation functions
│   ├── routers/
│   │   ├── annalakshmi.py   # CRUD + list/filter/paginate routes
│   │   └── dashboard.py     # Summary stats route
│   ├── static/               # CSS/JS (frontend, in progress)
│   └── templates/            # Jinja2 HTML pages (frontend, in progress)
├── tests/
│   └── test_annalakshmi.py  # End-to-end API tests
├── seed.py                   # Sample data seeding script
├── requirements.txt
├── README.md
└── annalakshmi.db
```

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/uhmd410/annalakshmi-dms.git
cd annalakshmi-dms

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
uvicorn app.main:app --reload

# 5. (Optional) Seed sample data
python seed.py
```

Once running:
- API root / health check: `http://127.0.0.1:8000/`
- Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`

---

## Database Schema

| Field | Column | Type | Constraints |
|---|---|---|---|
| Full Name | `full_name` | String(150) | Not null, min 2 chars |
| Mobile Number | `mobile_number` | String(15) | Not null, unique, indexed, 10-digit Indian format |
| Email Address | `email` | String(150) | Nullable, valid email format if present |
| Residential Address | `address` | String(300) | Not null, min 5 chars |
| Area / Locality | `area` | String(100) | Not null, indexed |
| City | `city` | String(100) | Not null |
| State | `state` | String(100) | Not null |
| PIN Code | `pin_code` | String(10) | Not null, 6-digit format |
| Cuisine Specialization | `cuisine_specialization` | String(150) | Not null |
| Veg / Non-Veg | `veg_or_nonveg` | String(10) | Not null, one of `veg` / `non-veg` |
| Signature Dishes | `signature_dishes` | String(500) | Nullable |
| Available Timings | `available_timings` | String(200) | Nullable |
| Maximum Orders Per Day | `max_orders_per_day` | Integer | Not null, default 10, must be > 0 |
| Date Joined | `date_joined` | Date | Not null, cannot be in the future |
| Current Status | `status` | String(10) | Not null, default `active`, indexed, one of `active` / `inactive` |
| — | `id` | Integer | Primary key, autoincrement |
| — | `created_at` | DateTime | Not null, set on insert |
| — | `updated_at` | DateTime | Not null, refreshed on every update |

---

## API Reference

All error responses share this shape:
```json
{
  "error": true,
  "message": "Human-readable summary",
  "details": [ { "field": "mobile_number", "message": "..." } ]
}
```
`details` is only present for validation errors (HTTP 422).

### Create a record
```
POST /annalakshmis/
```
**Body:**
```json
{
  "full_name": "Lakshmi Narayanan",
  "mobile_number": "9876543210",
  "email": "lakshmi.n@example.com",
  "address": "12, 4th Cross, Jayanagar",
  "area": "Jayanagar",
  "city": "Bangalore",
  "state": "Karnataka",
  "pin_code": "560041",
  "cuisine_specialization": "South Indian",
  "veg_or_nonveg": "veg",
  "signature_dishes": "Idli, Sambar, Coconut Chutney",
  "available_timings": "8 AM - 12 PM, 6 PM - 9 PM",
  "max_orders_per_day": 15,
  "date_joined": "2026-01-10",
  "status": "active"
}
```
Returns `200` with the created record (including `id`, `created_at`, `updated_at`), or `400` if `mobile_number` is already registered, or `422` on invalid input.

### List / search / filter / paginate
```
GET /annalakshmis/?name=&mobile=&area=&status=&page=1&page_size=10
```
All query params are optional and combinable. `page` and `page_size` default to `1` and `10` (`page_size` capped at 100).

**Response:**
```json
{
  "total": 42,
  "page": 1,
  "page_size": 10,
  "total_pages": 5,
  "items": [ { "id": 1, "full_name": "...", "...": "..." } ]
}
```

### Get a single record
```
GET /annalakshmis/{id}
```
Returns `200` with the full record, or `404` if not found.

### Update a record
```
PUT /annalakshmis/{id}
```
Body: any subset of fields (partial update supported). Returns `400` if changing `mobile_number` collides with a different existing record, `404` if the id doesn't exist.

### Archive a record (soft delete)
```
PATCH /annalakshmis/{id}/archive
```
Sets `status` to `"inactive"`. Idempotent — archiving an already-inactive record still returns `200`.

### Dashboard summary
```
GET /dashboard/summary
```
```json
{ "total": 42, "active": 38, "inactive": 4 }
```

---

## Validation Rules

| Field | Rule |
|---|---|
| `mobile_number` | Exactly 10 digits, starts with 6-9, must be unique |
| `email` | Valid email format if provided |
| `pin_code` | Exactly 6 digits |
| `full_name`, `address`, `area`, `city`, `state`, `cuisine_specialization` | Required, non-blank, length-limited |
| `max_orders_per_day` | Integer, must be > 0 and ≤ 200 |
| `date_joined` | Cannot be a future date |
| `veg_or_nonveg` | Must be exactly `"veg"` or `"non-veg"` |
| `status` | Must be exactly `"active"` or `"inactive"` |

---

## Testing

```bash
pytest -v
```

Tests run against an isolated `test.db`, torn down after each test — your dev database and seeded data are untouched. Covers: create, duplicate-mobile rejection, validation failures (email/mobile/PIN), get-by-id (found and not-found), update, idempotent archive, pagination, filtering, and dashboard summary.

---

## Assumptions Made

1. Mobile numbers follow the Indian 10-digit format (starting 6-9); international numbers aren't currently supported.
2. `email`, `signature_dishes`, and `available_timings` are optional since a homemaker may not have all three at onboarding time.
3. `signature_dishes` is stored as a single comma-separated string rather than a related table — sufficient for V1 display and substring search.
4. Archiving is a soft delete (status flip); records are never physically removed.
5. `date_joined` cannot be set in the future, since it represents an actual onboarding event.
6. Pagination defaults to 10 records per page, capped at 100 per request.
