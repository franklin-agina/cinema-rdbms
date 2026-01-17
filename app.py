"""
Cinema RDBMS – Flask + MySQL
Author: Franklin Okoth Agina
AI assistance: ChatGPT (guidance and review)

This application demonstrates:
- Relational database design
- Primary and foreign keys
- SQL JOIN queries
- CRUD operations
"""

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# -----------------------------
# Database connection
# -----------------------------

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="cinema_user",
        password="cinema_pass",
        database="cinema_db"
    )

# -----------------------------
# Movies CRUD
# -----------------------------

@app.route("/movies", methods=["POST"])
def create_movie():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO movies (title, duration_minutes) VALUES (%s, %s)",
        (data["title"], data["duration_minutes"])
    )
    db.commit()
    movie_id = cur.lastrowid
    cur.close()
    db.close()
    return jsonify({"id": movie_id, **data}), 201


@app.route("/movies", methods=["GET"])
def list_movies():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM movies")
    movies = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(movies)

# -----------------------------
# Screens CRUD
# -----------------------------

@app.route("/screens", methods=["POST"])
def create_screen():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO screens (name, capacity) VALUES (%s, %s)",
        (data["name"], data["capacity"])
    )
    db.commit()
    screen_id = cur.lastrowid
    cur.close()
    db.close()
    return jsonify({"id": screen_id, **data}), 201


@app.route("/screens", methods=["GET"])
def list_screens():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM screens")
    screens = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(screens)

# -----------------------------
# Showtimes (JOIN demo)
# -----------------------------

@app.route("/showtimes", methods=["POST"])
def create_showtime():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        INSERT INTO showtimes (movie_id, screen_id, start_time)
        VALUES (%s, %s, %s)
        """,
        (data["movie_id"], data["screen_id"], data["start_time"])
    )
    db.commit()
    showtime_id = cur.lastrowid
    cur.close()
    db.close()
    return jsonify({"id": showtime_id, **data}), 201


@app.route("/showtimes", methods=["GET"])
def list_showtimes():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        """
        SELECT
            s.id,
            m.title AS movie,
            sc.name AS screen,
            s.start_time
        FROM showtimes s
        JOIN movies m ON s.movie_id = m.id
        JOIN screens sc ON s.screen_id = sc.id
        ORDER BY s.start_time
        """
    )
    showtimes = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(showtimes)

# -----------------------------
# Bookings (multi-table JOIN)
# -----------------------------

@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        INSERT INTO bookings (showtime_id, customer_name, seats)
        VALUES (%s, %s, %s)
        """,
        (data["showtime_id"], data["customer_name"], data["seats"])
    )
    db.commit()
    booking_id = cur.lastrowid
    cur.close()
    db.close()
    return jsonify({"id": booking_id, **data}), 201


@app.route("/bookings", methods=["GET"])
def list_bookings():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        """
        SELECT
            b.id,
            b.customer_name,
            b.seats,
            m.title AS movie,
            sc.name AS screen,
            s.start_time
        FROM bookings b
        JOIN showtimes s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN screens sc ON s.screen_id = sc.id
        ORDER BY s.start_time
        """
    )
    bookings = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(bookings)

# -----------------------------
# Run application
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
