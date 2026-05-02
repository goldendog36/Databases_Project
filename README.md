# Databases_Project

Setup:
-----------------------------------------------------------
To setup the database on a linux based machine, you should be able to just run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 setup.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Then enter your passwords when prompted.

If on a Windows/MacOS machine, use other_setup.py and find
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        password="rootuser1234",
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
on line 40 of other_setup.py. Replace the words in 
quotations with your mysql password for your 'root'@'localhost'

Before running the actual script, find
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        password = "ENTER YOUR PASSWORD",
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
in line 7 at db.py and replace the words in quotations with your mysql password for your 'root'@'localhost'

Run
----------------------------------------------------------
After all that setup is done, run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 cli.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
to start the program.

Library Dependencies:
kagglehub
subprocess
sys
mysql, mysql.connector

to install dependencies, run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pip install kagglehub mysql-connector-python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
