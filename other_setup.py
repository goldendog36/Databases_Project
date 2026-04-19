import kagglehub
import os
import shutil

# 1. Setup folders
project_dir = os.getcwd()
data_dir = os.path.join(project_dir, "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 2. Download from Kaggle
print("Downloading data from Kaggle...")
path1_src = kagglehub.dataset_download("alexanderxela/sp-500-companies")
path2_src = kagglehub.dataset_download("jacksaleeby/s-and-p500-historical-data")

# 3. Enhanced Find and Move function
def move_csv(src_folder, dest_folder, label):
    print(f"\nSearching for {label} in: {src_folder}")
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            print(f"  - Found file: {file}") # This shows us every file it sees
            if file.endswith(".csv"):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, file)
                shutil.copy(src_path, dest_path)
                print(f"  SUCCESS: Moved {file} to {dest_folder}")
                return dest_path
    return None

# 4. Assign the paths
path1 = move_csv(path1_src, data_dir, "Company Data")
path2 = move_csv(path2_src, data_dir, "Historical Price Data")

# 5. Check and Replace
if path1 and path2:
    with open("other_tables.sql", "r") as file:
        sql_content = file.read()

    # Final verification of the strings
    sql_content = sql_content.replace("{{path1}}", path1).replace("{{path2}}", path2)

    with open("temp_tables.sql", "w") as file:
        file.write(sql_content)

    print("\n" + "="*30)
    print("SETUP SUCCESSFUL")
    print("="*30)
    print(f"SQL file created: temp_tables.sql")
    print(f"Data folder: {data_dir}")
    print("\nRun this command in your terminal to build the DB:")
    print("mysql --local-infile=1 -u root -p < temp_tables.sql")
else:
    print("\n" + "!"*30)
    print("CRITICAL ERROR: CSVs NOT FOUND")
    print("!"*30)
    print("Check the 'Found file' list above to see what was actually downloaded.")