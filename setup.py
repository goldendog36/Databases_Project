import kagglehub
import subprocess

# download dataset
path1 = kagglehub.dataset_download("alexanderxela/sp-500-companies")
path2 = kagglehub.dataset_download("jacksaleeby/s-and-p500-historical-data")

# move files to mysql-files directory
subprocess.run(["sudo", "mv", path1, "/var/lib/mysql-files/"])
subprocess.run(["sudo", "mv", path2, "/var/lib/mysql-files/"])

cmd = f"""
sed "s|{{{{path1}}}}|{path1}|g; s|{{{{path2}}}}|{path2}|g" tables.sql |
mysql -u root -p SP500_Analysis
"""

subprocess.run(cmd, shell=True, executable="/bin/bash")

# Old run code.
# subprocess.run(["sudo", "mysql", "-u", "root", "<", "tables.sql"])
