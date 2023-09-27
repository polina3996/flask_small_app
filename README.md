BATUMI RESTAURANTS REVIEW APP

The basic application that illustrates six most popular restaurants in Batumi, Georgia and gives a client the opportunity to contact with it. 

The client can registrate, leave a feedback and see other feedbacks. 

All users and feedbacks are stored in a database (based on SQLite3). 

<b>Start</b>

Create 'instance' directory in the core of the project.
Create 'config.py' file in it with the following data:
- SECRET_KEY = <random string> ($ python -c 'import secrets; print(secrets.token_hex()))
- DATABASE = 'instance/flask_small_app.sqlite'

In terminal print: flask init-db .

After the file 'flask_small_app.sqlite' in 'instance' directory was created, print: flask --app app run

