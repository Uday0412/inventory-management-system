# Inventory Management System (FastAPI)

## Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Run from the project root (recommended)
uvicorn app.main:app --reload

# OR if you are inside the app/ folder:
# uvicorn main:app --reload
```

Open:
- `http://127.0.0.1:8000/docs`

## Environment

`.env` (already in this repo) supports:
- `app_name`
- `database_url` (default: `sqlite:///./test.db`)

## API (Inventory)

Base path: `/inventory`

- `GET /inventory/categories`
- `POST /inventory/categories`
- `PATCH /inventory/categories/{category_id}`
- `DELETE /inventory/categories/{category_id}`

- `GET /inventory/items`
- `POST /inventory/items`
- `PATCH /inventory/items/{item_id}`
- `DELETE /inventory/items/{item_id}`

- `POST /inventory/items/{item_id}/adjust` (stock in/out)
- `GET /inventory/items/{item_id}/movements`

