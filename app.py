from ast import Global, Pass
from datetime import datetime
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
    c = sqlite3.connect('database.db')
    cur = c.cursor()
    cur.execute("SELECT * from Albums")
    
    return render_template('home.html', test = cur.fetchall())

@app.route('/album_insert')
def album_insert():
    new_row = [request.args['title'],request.args['artist'],datetime.strptime(request.args['released'], '%Y-%m-%d')]
    DB.session.add(Albums(title=new_row[0], artist=new_row[1], released=new_row[2]))
    DB.session.commit()
    return render_template('insert.html', new_row=new_row)

@app.route('/insert')
def insert():
    
    return request.args['released']
                               
@app.route('/reset')
def reset():
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    return 'Data base was re-established'


if __name__ == '__main__':
    app.run()
