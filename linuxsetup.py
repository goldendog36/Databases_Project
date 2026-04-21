import kagglehub
import subprocess

path1 = kagglehub.dataset_download("alexanderxela/sp-500-companies", force_download=True)
path2 = kagglehub.dataset_download("jacksaleeby/s-and-p500-historical-data", force_download=True)

subprocess.run(["sudo", "mv", path1 + "/sp500-companies.csv", "/var/lib/mysql-files/"])
subprocess.run(["sudo", "mv", path2 + "/SP500_Historical_Data.csv", "/var/lib/mysql-files/"])

subprocess.run("mysql -u root -p SP500_Analysis < linuxtables.sql", shell=True, executable="/bin/bash")

