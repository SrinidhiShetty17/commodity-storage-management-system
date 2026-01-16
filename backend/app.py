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



from datetime import datetime

@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json()

    # Validate input
    required_fields = [
        "factory_id",
        "commodity_id",
        "quantity",
        "transaction_type",
        "transaction_date"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if data["transaction_type"] not in ["IN", "OUT"]:
        return jsonify({"error": "transaction_type must be IN or OUT"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO transactions
        (factory_id, commodity_id, quantity, transaction_type, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["factory_id"],
            data["commodity_id"],
            data["quantity"],
            data["transaction_type"],
            data["transaction_date"]
        ))

        conn.commit()

        return jsonify({"message": "Transaction recorded successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append({
            "transaction_id": r[0],
            "factory_id": r[1],
            "commodity_id": r[2],
            "quantity": r[3],
            "transaction_type": r[4],
            "transaction_date": r[5]
        })

    cursor.close()
    conn.close()
    return jsonify(result)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT
            f.factory_id,
            f.factory_name,
            c.commodity_id,
            c.commodity_name,
            SUM(
                CASE
                    WHEN t.transaction_type = 'IN' THEN t.quantity
                    WHEN t.transaction_type = 'OUT' THEN -t.quantity
                END
            ) AS current_stock
        FROM transactions t
        JOIN factories f ON t.factory_id = f.factory_id
        JOIN commodities c ON t.commodity_id = c.commodity_id
        GROUP BY
            f.factory_id, f.factory_name,
            c.commodity_id, c.commodity_name
        ORDER BY f.factory_id, c.commodity_id;
    """

    cur.execute(query)
    rows = cur.fetchall()

    inventory = []
    for row in rows:
        inventory.append({
            "factory_id": row[0],
            "factory_name": row[1],
            "commodity_id": row[2],
            "commodity_name": row[3],
            "current_stock": row[4]
        })

    cur.close()
    conn.close()

    return jsonify(inventory), 200



if __name__ == "__main__":
    app.run(debug=True)