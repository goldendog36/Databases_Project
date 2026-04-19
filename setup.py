import kagglehub
import subprocess

path1 = kagglehub.dataset_download("alexanderxela/sp-500-companies")
path2 = kagglehub.dataset_download("jacksaleeby/s-and-p500-historical-data")

subprocess.run(["sudo", "mv", path1 + "/sp500-companies.csv", "/var/lib/mysql-files/sp500-companies.csv"])
subprocess.run(["sudo", "mv", path2 + "/SP500_Historical_Data.csv", "/var/lib/mysql-files/SP500_Historical_Data.csv"])

subprocess.run("mysql -u root -p SP500_Analysis < tables.sql", shell=True, executable="/bin/bash")

# Old run code.
# subprocess.run(["sudo", "mysql", "-u", "root", "<", "tables.sql"])
