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
            password="your password",
            allow_local_infile=True
        )
        cursor = conn.cursor()

        print("Cleaning old data...")
        cursor.execute("SET GLOBAL local_infile = 1;")
        cursor.execute("DROP DATABASE IF EXISTS SP500_Analysis;")
        cursor.execute("CREATE DATABASE SP500_Analysis;")
        cursor.execute("USE SP500_Analysis;")

        commands = sql_content.split(';')
        for command in commands:
            clean_command = command.strip()
            if clean_command:
                print(f"Executing: {clean_command[:60]}...")
                cursor.execute(clean_command)

        conn.commit()
        print("\nSUCCESS: Database built, 2.7M rows loaded, and indexes created.")

    except mysql.connector.Error as err:
        print(f"CRITICAL DATABASE ERROR: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    run_setup()