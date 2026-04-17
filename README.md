# Databases_Project

Setup:
-----------------------------------------------------------
To setup the database, you should be able to just run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 setup.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Then enter your passwords when prompted.

Before running the actual script, find
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        password = "ENTER YOUR PASSWORD",
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
in cli.py at the top. Replace The words in quotations with your mysql password for your 'root'@'localhost'

Run
----------------------------------------------------------
After all that setup is done, run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 cli.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
to start the program.

Other Stuff
----------------------------------------------------------
We will be doing our databases project and uploading important files to it here! Huzzah! Yippee!

I made it a lot more efficient since last time but it still takes a while to calculate the 14-day rsi values so I might update that implementation to be a python script in setup.py.

We no longer need to bundle either sheet of data in with the project because it gets downloaded by the user during setup.py and moved to their library of mysql-files. Specifically: /var/lib/mysql-files/

Library Dependencies:
kagglehub
subprocess
sys
mysql, mysql.connector
