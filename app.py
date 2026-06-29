import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

app = Flask(__name__)
# Re-render templates on every request during development.
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ---------------------------------------------------------------------------
# MongoDB Atlas connection
# ---------------------------------------------------------------------------
# Set MONGODB_URI in a .env file (see .env.example). The connection is created
# lazily so the app can still boot (and serve /api) even without a database.
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB", "flaskProject")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION", "submissions")

_client = None


def get_collection():
    """Return the MongoDB collection, creating the client on first use."""
    global _client
    if not MONGODB_URI:
        raise RuntimeError(
            "MONGODB_URI is not configured. Add it to your .env file."
        )
    if _client is None:
        # serverSelectionTimeoutMS keeps failed connections from hanging.
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    return _client[DB_NAME][COLLECTION_NAME]


# ---------------------------------------------------------------------------
# Task 1: /api reads a JSON list from a backend file and returns it.
# ---------------------------------------------------------------------------
@app.route("/api")
def api():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)


# ---------------------------------------------------------------------------
# Task 2: A form that inserts data into MongoDB Atlas.
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            # Validation error: stay on the page and show the error.
            return render_template(
                "form.html", error="Name and email are required.",
            )

        try:
            get_collection().insert_one(
                {"name": name, "email": email, "message": message}
            )
        except (PyMongoError, RuntimeError) as exc:
            # Submission error: stay on the page and show the error.
            return render_template("form.html", error=str(exc))

        # Success: redirect to the success page.
        return redirect(url_for("success"))

    return render_template("form.html")


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
