from flask import Flask, jsonify, request
import mysql.connector

def success_response(data=None, message=None, status=200):
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    return jsonify(response), status


def error_response(message, status=400):
    return jsonify({
        "success": False,
        "error": message
    }), status

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

@app.route('/commodities', methods=['GET'])
def get_commodities():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT commodity_id, commodity_name FROM commodities")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "name": r[1]
        })

    return success_response(data=result)


@app.route('/commodities', methods=['POST'])
def add_commodity():
    data = request.json

    if not data or 'name' not in data:
        return error_response("Commodity name is required")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO commodities (name) VALUES (%s)",
            (data['name'],)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        return error_response("Commodity already exists", 400)
    finally:
        cursor.close()
        conn.close()

    return success_response(
        message="Commodity added successfully",
        status=201
    )


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
@app.route('/transactions', methods=['POST'])
def add_transaction():
    #   JSON body
    if not request.is_json:
        return error_response("JSON body required", 400)

    data = request.json

    #  Required fields check
    required_fields = [
        "commodity_id",
        "transaction_type",
        "quantity",
        "transaction_date"
    ]

    for field in required_fields:
        if field not in data:
            return error_response(f"{field} is required", 400)

    #  Validate transaction_type
    transaction_type = data["transaction_type"]
    if transaction_type not in ["IN", "OUT"]:
        return error_response("transaction_type must be IN or OUT", 400)

    #  Validate quantity
    try:
        quantity = int(data["quantity"])
        if quantity <= 0:
            return error_response("quantity must be greater than 0", 400)
    except:
        return error_response("quantity must be an integer", 400)

    #  Validate commodity_id
    try:
        commodity_id = int(data["commodity_id"])
    except:
        return error_response("commodity_id must be an integer", 400)

    transaction_date = data["transaction_date"]

    #  DB connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        #  Get available stock up to transaction_date
        available_stock = get_available_stock(
            cursor,
            commodity_id,
            transaction_date
        )

        #  Validate OUT transaction
        if transaction_type == "OUT" and quantity > available_stock:
            return error_response(
                f"Insufficient stock. Available stock: {available_stock}",
                400
            )

        #  Insert transaction
        insert_query = """
            INSERT INTO transactions
            (commodity_id, transaction_type, quantity, transaction_date)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            commodity_id,
            transaction_type,
            quantity,
            transaction_date
        ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Transaction Error:", e)
        return error_response("Failed to record transaction", 500)

    finally:
        cursor.close()
        conn.close()

    # 🔟 Success response
    return success_response(
        message="Transaction recorded successfully",
        status=201
    )



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
        c.commodity_name,
        t.commodity_id,
        YEAR(t.transaction_date) AS year,
        MONTH(t.transaction_date) AS month,
        SUM(
            CASE
                WHEN t.transaction_type = 'IN' THEN t.quantity
                WHEN t.transaction_type = 'OUT' THEN -t.quantity
            END
        ) AS net_quantity
    FROM transactions t
    JOIN commodities c ON t.commodity_id = c.commodity_id
    GROUP BY
        c.commodity_name,
        t.commodity_id,
        YEAR(t.transaction_date),
        MONTH(t.transaction_date)
    ORDER BY
        c.commodity_name,
        year,
        month;
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
        c.commodity_name,
        t.commodity_id,
        YEAR(t.transaction_date) AS year,
        MONTH(t.transaction_date) AS month,
        SUM(
            CASE
                WHEN t.transaction_type = 'IN' THEN t.quantity
                WHEN t.transaction_type = 'OUT' THEN -t.quantity
            END
        ) AS net_quantity
    FROM transactions t
    JOIN commodities c ON t.commodity_id = c.commodity_id
    GROUP BY
        c.commodity_name,
        t.commodity_id,
        YEAR(t.transaction_date),
        MONTH(t.transaction_date)
    ORDER BY
        c.commodity_name,
        year,
        month;
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
            "commodity_name": row["commodity_name"],
            "year": row["year"],
            "month": row["month"],
            "net_quantity": int(row["net_quantity"]),
            "closing_stock": stock_tracker[key]
        })

    return jsonify(result), 200

@app.errorhandler(Exception)
def handle_exception(e):
    print("ERROR:", str(e))  # log to console
    return error_response("Internal server error", 500)

if __name__ == "__main__":
    app.run(debug=True)