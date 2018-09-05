
# Dependencies
pip install google-api-python-client
pip install mysql-connector-python 8.0.12
pip install mysqlclient 1.3.10
pip install oauth2client 2.2.0
pip install oauthlib 2.0.6

Update the query parameter in gmailAi.py file 
Dump the dump.sql file to get the db schema and update the username and password of db in both py files
Run gmailAi.py using '''python gmailAi.py''''
It will prompt for authentication through browser.
Provide access and close the window.
Now database will be filled the values
Based on your prefernce update the rules.json file and run rules.py file
The actions are performed on the corresponding e-mails
