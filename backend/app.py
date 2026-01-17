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

    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔹 Calculate current stock
    cursor.execute(
        """
        SELECT COALESCE(
            SUM(
                CASE
                    WHEN transaction_type = 'IN' THEN quantity
                    WHEN transaction_type = 'OUT' THEN -quantity
                END
            ), 0)
        FROM transactions
        WHERE factory_id = %s AND commodity_id = %s;
        """,
        (data["factory_id"], data["commodity_id"])
    )

    current_stock = cursor.fetchone()[0]

    # 🔒 Stock validation
    if data["transaction_type"] == "OUT" and data["quantity"] > current_stock:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Insufficient stock",
            "available_stock": current_stock
        }), 400

    # ✅ Insert transaction
    cursor.execute(
        """
        INSERT INTO transactions
        (factory_id, commodity_id, quantity, transaction_type, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data["factory_id"],
            data["commodity_id"],
            data["quantity"],
            data["transaction_type"],
            data["transaction_date"]
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Transaction recorded successfully"}), 201


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

@app.route("/reports/daily", methods=["GET"])
def daily_report():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            DATE(t.transaction_date) AS date,
            f.factory_name,
            c.commodity_name,
            SUM(CASE WHEN t.transaction_type = 'IN' THEN t.quantity ELSE 0 END) AS total_in,
            SUM(CASE WHEN t.transaction_type = 'OUT' THEN t.quantity ELSE 0 END) AS total_out,
            SUM(
                CASE
                    WHEN t.transaction_type = 'IN' THEN t.quantity
                    WHEN t.transaction_type = 'OUT' THEN -t.quantity
                END
            ) AS net_movement
        FROM transactions t
        JOIN factories f ON t.factory_id = f.factory_id
        JOIN commodities c ON t.commodity_id = c.commodity_id
        GROUP BY DATE(t.transaction_date), f.factory_name, c.commodity_name
        ORDER BY date DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    report = []
    for r in rows:
        report.append({
            "date": str(r[0]),
            "factory_name": r[1],
            "commodity_name": r[2],
            "total_in": r[3],
            "total_out": r[4],
            "net_movement": r[5]
        })

    cursor.close()
    conn.close()

    return jsonify(report), 200
@app.route('/reports/monthly', methods=['GET'])
def monthly_report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
    commodity_id,
    YEAR(transaction_date) AS year,
    MONTH(transaction_date) AS month,
    SUM(
        CASE
            WHEN transaction_type = 'IN' THEN quantity
            WHEN transaction_type = 'OUT' THEN -quantity
        END
    ) AS net_quantity
FROM transactions
GROUP BY commodity_id, YEAR(transaction_date), MONTH(transaction_date)
ORDER BY year DESC, month DESC;

"""
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(result), 200

@app.route("/reports/monthly-closing", methods=["GET"])
def monthly_closing_report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            commodity_id,
            YEAR(transaction_date) AS year,
            MONTH(transaction_date) AS month,
            SUM(
                CASE
                    WHEN transaction_type = 'IN' THEN quantity
                    WHEN transaction_type = 'OUT' THEN -quantity
                END
            ) AS net_quantity
        FROM transactions
        GROUP BY commodity_id, YEAR(transaction_date), MONTH(transaction_date)
        ORDER BY commodity_id, year, month;
    """

    cursor.execute(query)
    monthly_data = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []
    stock_tracker = {}

    for row in monthly_data:
        key = (row["commodity_id"], row["year"])

        if key not in stock_tracker:
            stock_tracker[key] = 0

        stock_tracker[key] += int(row["net_quantity"])

        result.append({
            "commodity_id": row["commodity_id"],
            "year": row["year"],
            "month": row["month"],
            "net_quantity": int(row["net_quantity"]),
            "closing_stock": stock_tracker[key]
        })

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)