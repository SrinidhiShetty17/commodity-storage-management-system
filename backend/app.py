from flask import Flask, jsonify
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
@app.route("/factories", methods=["GET"])
def get_factories():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT factory_id, factory_name, location
        FROM factories
    """)

    factories = cursor.fetchall()

    result = []
    for f in factories:
        result.append({
            "factory_id": f[0],
            "factory_name": f[1],
            "location": f[2]
        })

    cursor.close()
    conn.close()

    return jsonify(result)

# ---------- ROOT CHECK ----------
@app.route("/")
def home():
    return {"status": "Backend running successfully"}

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)
