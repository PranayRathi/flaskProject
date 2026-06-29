# flaskProject

A simple Flask app with two features:

1. **`/api`** — returns a JSON list read from a backend file (`data.json`).
2. **Form (`/`)** — submits data to MongoDB Atlas. On success it redirects to a
   "Data submitted successfully" page; on error it shows the error on the same page.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your MongoDB Atlas connection string:

```
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=flaskProject
MONGODB_COLLECTION=submissions
```

## Run

```bash
python3 app.py
```

Then open:

- Form: http://localhost:5001
- API: http://localhost:5001/api

The server auto-reloads when you save changes (debug mode).

## Project structure

```
flaskProject/
├── app.py              # Flask routes (/api, form, MongoDB insert)
├── data.json           # Backend JSON list served by /api
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── form.html
│   └── success.html
└── README.md
```
