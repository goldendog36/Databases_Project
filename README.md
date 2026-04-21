# Databases_Project

Setup:
-----------------------------------------------------------
Before setting up the database, find
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        password="rootuser1234",
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
around line 46 of other_setup.py. Replace the words in 
quotations with your mysql password for your 'root'@'localhost'

Then run with:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 setup.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If setup fails for linux users try:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 linuxsetup.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Then enter your sudo password and your mysql password for your
'root'@'localhost' when prompted

See Troubleshooting if that still fails, otherwise continue.

Before running the actual script, find
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        password = "ENTER YOUR PASSWORD",
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
in db.py at the top. Replace The words in quotations with your
mysql password for your 'root'@'localhost'

Run
----------------------------------------------------------
After all that setup is done, run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 cli.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
to start the program.

Troubleshooting
----------------------------------------------------------
If the files are not downloading, try manually downloading
them from,
https://www.kaggle.com/datasets/jacksaleeby/s-and-p500-historical-data
and
https://www.kaggle.com/datasets/alexanderxela/sp-500-companies
Then move the files manually into ~/var/lib/mysql-files/
Then run:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mysql -u root -p SP500_Analysis < linuxtables.sql
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If that fails then the problem is with how you have your mysql
set up. Please make sure it is set up correct and retry.

Other Stuff
----------------------------------------------------------
We will be doing our databases project and uploading important files to it here! Huzzah! Yippee!

I made it a lot more efficient since last time but it still takes a while to calculate the 14-day rsi values so I might update that implementation to be a python script in setup.py.

We no longer need to bundle either sheet of data in with the project because it gets downloaded by the user during setup.py and moved to their library of mysql-files. Specifically: /var/lib/mysql-files/

Library Dependencies
----------------------------------------------------------
kagglehub
subprocess
sys
mysql, mysql.connector
