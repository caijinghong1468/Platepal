import os
from database import db
from dotenv import load_dotenv
from flask import Flask, jsonify, abort
from user import user
from goal import goal
from meal import meal
from group import group
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def initialize_app():
    # Initialize the app with the current amount of each goal
    with app.app_context():
        try:
            print(db.connection.cursor())
            cursor = db.connection.cursor()
           
        except:
            cursor.execute("ROLLBACK")
            cursor.close()
            abort(500, "ERROR 500")
    
load_dotenv()

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

db.init_app(app)
initialize_app() # Initialize the app with the current amount of each goal
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(meal, url_prefix="/meal")
app.register_blueprint(goal, url_prefix="/goal")
app.register_blueprint(group, url_prefix="/group")


@app.route('/')
def home():
    return render_template('index.html')  # Serve the main page

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000, debug=True)