import kagglehub
import os
import shutil
import mysql.connector
from db import connect


def run_setup():
    project_dir = os.getcwd()
    data_dir = os.path.join(project_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    print("Downloading data...")
    path1_src = kagglehub.dataset_download("alexanderxela/sp-500-companies")
    path2_src = kagglehub.dataset_download("jacksaleeby/s-and-p500-historical-data")

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

    with open("other_tables.sql", "r") as f:
        sql_content = f.read()

    sql_content = sql_content.replace("{{path1}}", path1).replace("{{path2}}", path2)

    print("Connecting to MySQL to build database...")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR PASSWORD HERE",
            allow_local_infile=True
        )
        cursor = conn.cursor()

        cursor.execute("SET GLOBAL local_infile = 1;")

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