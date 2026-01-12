from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# -------------------------------
# Database Connection
# -------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sri1703!",
        database="commodity_storage"
    )

# -------------------------------
# Home Route
# -------------------------------
@app.route("/")
def home():
    return "Commodity Storage Backend Running"

# -------------------------------
# GET Factories API
# -------------------------------
@app.route("/factories", methods=["GET"])
def get_factories():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT factory_id, factory_name, city FROM factories"
    )

    factories = cursor.fetchall()

    result = []
    for f in factories:
        result.append({
            "factory_id": f[0],
            "factory_name": f[1],
            "city": f[2]
        })

    cursor.close()
    conn.close()

    return jsonify(result)

# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
