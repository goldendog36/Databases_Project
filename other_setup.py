import kagglehub
import os
import shutil
import mysql.connector
from db import connect  # Uses your existing connection logic


def run_setup():
    # 1. Folders and Downloads
    project_dir = os.getcwd()
    data_dir = os.path.join(project_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    print("Downloading data...")
    path1_src = kagglehub.dataset_download("alexanderxela/sp-500-companies")
    path2_src = kagglehub.dataset_download("jacksaleeby/s-and-p500-historical-data")

    # 2. Find and Copy Files (The 'Walk' logic we fixed)
    def get_path(src):
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.lower().endswith(".csv"):
                    dest = os.path.join(data_dir, file)
                    shutil.copy(os.path.join(root, file), dest)
                    return dest
        return None

    path1 = get_path(path1_src)
    path2 = get_path(path2_src)

    # 3. Prepare SQL Content
    with open("other_tables.sql", "r") as f:
        sql_content = f.read()

    # Replace placeholders with absolute paths
    sql_content = sql_content.replace("{{path1}}", path1).replace("{{path2}}", path2)

    # 4. AUTOMATIC EXECUTION
    print("Connecting to MySQL to build database...")
    try:
        # We need allow_local_infile=True for the LOAD DATA command to work in Python
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootuser1234",  # Use your specific password here
            allow_local_infile=True
        )
        cursor = conn.cursor()

        # Enable local infile on the server session
        cursor.execute("SET GLOBAL local_infile = 1;")

        # Split the SQL file into individual commands
        # MySQL Connector cannot execute multiple statements at once by default
        commands = sql_content.split(';')

        for command in commands:
            if command.strip():
                print(f"Executing: {command[:50]}...")
                cursor.execute(command)

        conn.commit()
        print("Database built and indexed successfully.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    run_setup()