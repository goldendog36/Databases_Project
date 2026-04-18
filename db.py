import mysql.connector

def connect():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "ENTER YOUR PASSWORD",
        database = "SP500_Analysis"
    )

def execute_query(cursor, query, params=None):
    try: 
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None