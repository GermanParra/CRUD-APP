import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import DB, Albums, Tracks

app = Flask(__name__)


# Database configurations
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Turn off verification when we request changes to db
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db' #getenv('DATABASE_URI')

# Connect DB to Flask app
DB.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/edit', methods=['GET','POST'])
def edit():
    
    return jsonify(title=request.args['title'],
                   artist=request.args['artist'],
                   released=request.args['released'])
                               
@app.route('/reset')
def reset():
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    return 'Data base was re-established'


if __name__ == '__main__':
    app.run()
