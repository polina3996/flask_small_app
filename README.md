flask_small_app

The basic application that illustrates six most popular restaurants in Batumi, Georgia and gives a client the opportunity to contact with it.
The client can registrate, leave a feedback and see other feedbacks. All users and feedbacks are stored in a database (based on SQLite3).

Install

Be sure to use the same version of the code as the version of the docs you're reading. You probably want the latest tagged version, but the default Git version is the main branch.

# clone the repository
$ git clone https://github.com/polina3996/flask_small_app
$ cd flask
# checkout the correct version
$ git tag  # shows the tagged versions

$ git checkout latest-tag-found-above

$ cd examples/tutorial

Create a virtualenv and activate it:

$ python3 -m venv .venv

$ . .venv/bin/activate

Or on Windows cmd:

$ py -3 -m venv .venv

$ .venv\Scripts\activate.bat

Install flask-application:

$ pip install -e .

Or if you are using the main branch, install Flask from source before installing flask_small_app:

$ pip install -e ../..

$ pip install -e .

Run
$ flask --app flask_small_app init-db

$ flask --app flask_small_app run --debug

Open http://127.0.0.1:5000 in a browser.

Test

$ pip install '.[test]'

$ pytest

Run with coverage report:

$ coverage run -m pytest

$ coverage report

$ coverage html  # open htmlcov/index.html in a browser