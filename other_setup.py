import kagglehub
import os
import shutil

# 1. Get the current directory of the project
project_dir = os.getcwd()
data_dir = os.path.join(project_dir, "data")

# 2. Create a local 'data' folder if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 3. Download datasets
print("Downloading data from Kaggle...")
path1_src = kagglehub.dataset_download("alexanderxela/sp-500-companies")
path2_src = kagglehub.dataset_download("jacksaleeby/s-and-p500-historical-data")

# 4. Move files using shutil (Works on Windows, Mac, and Linux)
# We find the actual CSV inside the kagglehub folder
def move_csv(src_folder, dest_folder):
    for file in os.listdir(src_folder):
        if file.endswith(".csv"):
            shutil.move(os.path.join(src_folder, file), os.path.join(dest_folder, file))
            return os.path.join(dest_folder, file)

path1 = move_csv(path1_src, data_dir)
path2 = move_csv(path2_src, data_dir)

# 5. Prepare the SQL script using Python's string replacement (Replaces sed)
with open("other_tables.sql", "r") as file:
    sql_content = file.read()

# Swap the placeholders for the actual local paths
sql_content = sql_content.replace("{{path1}}", path1).replace("{{path2}}", path2)

with open("temp_tables.sql", "w") as file:
    file.write(sql_content)

print(f"Setup complete. Data is stored in {data_dir}")
print("Now run: mysql -u root -p SP500_Analysis < temp_tables.sql")