from flask_app import app
from flask_app.controllers import users, books

if __name__ == "__main__":
    app.run(debug=True)

# 1. create a folder for your project
# 2. create a virtual environment using the pipenv command pipenv install flask
# 3. pipenv shell turns on the virtual environment or shell
# 4. pip list (check to make sure that our dependencies are installed)
# 5. server.py
# 6. python3 server.py




# 1. Create a new DB or Schema in MySQL (ERD-->Forward Engineering)
# 2. Create a MySQL configuration file in the config folder
# 3. Create a User class in the models folder
# 4. Define class methods that run SQL queries against the DB