import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None
