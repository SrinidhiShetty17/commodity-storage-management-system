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

@app.route("/commodities", methods=["GET"])
def get_commodities():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM commodities")
    commodities = cursor.fetchall()

    result = []
    for c in commodities:
        result.append({
            "commodity_id": c[0],
            "commodity_name": c[1],
            "unit": c[2]
        })

    cursor.close()
    conn.close()

    return jsonify(result)

@app.route("/commodities", methods=["POST"])
def add_commodity():
    data = request.get_json()

    commodity_name = data.get("commodity_name")
    unit = data.get("unit")

    if not commodity_name or not unit:
        return jsonify({"error": "commodity_name and unit are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO commodities (commodity_name, unit) VALUES (%s, %s)",
        (commodity_name, unit)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Commodity added successfully"}), 201


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