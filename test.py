import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",        # e.g. "localhost"
    user="root",    # your MySQL username
    password="Password",
    database="SP500_Analysis"
)

cursor = conn.cursor()

# Execute query
query = "SELECT * FROM Trading_Signals LIMIT 2000"
cursor.execute(query)

# Fetch and print results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Clean up
cursor.close()
conn.close()