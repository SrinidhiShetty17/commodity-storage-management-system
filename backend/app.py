from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sri1703!",
        database="commodity_storage"
    )

# ---------- ROUTE: GET FACTORIES ----------
@app.route('/factories', methods=['GET', 'POST'])
def factories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------- GET ----------
    if request.method == 'GET':
        cursor.execute("SELECT * FROM factories")
        factories = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(factories)

    # ---------- POST ----------
    if request.method == 'POST':
        data = request.get_json()

        factory_name = data.get('factory_name')
        location = data.get('location')

        if not factory_name or not location:
            return jsonify({"error": "factory_name and location are required"}), 400

        cursor.execute(
            "INSERT INTO factories (factory_name, location) VALUES (%s, %s)",
            (factory_name, location)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Factory added successfully"}), 201


# ---------- ROOT CHECK ----------
@app.route("/")
def home():
    return {"status": "Backend running successfully"}

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/factories", methods=["POST"])
def add_factory():
    data = request.get_json()

    factory_name = data.get("factory_name")
    location = data.get("location")

    if not factory_name or not location:
        return jsonify({"error": "factory_name and location are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO factories (factory_name, location) VALUES (%s, %s)",
        (factory_name, location)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Factory added successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)