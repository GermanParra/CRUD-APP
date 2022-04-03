from datetime import datetime
import sqlite3
from flask import Flask, render_template, request #, redirect, url_for, jsonify
from models import DB, Albums, Tracks

app = Flask(__name__)


# Database configurations
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Turn off verification when we request changes to db
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db' #getenv('DATABASE_URI')

# Connect DB to Flask app
DB.init_app(app)


@app.route('/')
def home():
    # Extracting Info From Albums Table to create HTML table
    conection = sqlite3.connect('database.db')
    cursor = conection.cursor()
    albums = cursor.execute("SELECT * from Albums").fetchall()
    rows_count = cursor.execute("SELECT COUNT(*) from Albums").fetchall()
    
    return render_template('home.html', Albums = albums, Rows_count=rows_count)


@app.route('/album_insert', methods=['GET','POST'])
def album_insert():
    row_info=[]
    if request.method == 'POST':
        # Inserting New Row Info into Albums Table 
        row_info = [request.form['title'], request.form['artist'], datetime.strptime(request.form['released'], '%Y-%m-%d')]
        row = Albums(title=row_info[0], artist=row_info[1], released=row_info[2])
        DB.session.add(row)
        DB.session.commit()

    # Extracting Info From Albums Table to create HTML table
    conection = sqlite3.connect('database.db')
    cursor = conection.cursor()
    rows_count = cursor.execute("SELECT COUNT(*) from Albums").fetchall()
    albums = cursor.execute("SELECT * from Albums").fetchall()
    
    return render_template('insert.html', new_row_info=row_info, Albums = albums, Rows_count=rows_count)


@app.route('/reset', methods=['GET','POST'])
def reset():
    # Reseting Database
    DB.drop_all()
    DB.create_all()
    DB.session.commit()

    # Extracting Info From Albums Table to create HTML table
    conection = sqlite3.connect('database.db')
    cursor = conection.cursor()
    albums = cursor.execute("SELECT * from Albums").fetchall()
    rows_count = cursor.execute("SELECT COUNT(*) from Albums").fetchall()

    return render_template('reset.html', Albums = albums, Rows_count=rows_count)


@app.route('/edit', methods=['GET','POST'])
def edit():
    return request.form["ROW_ID"]


if __name__ == '__main__':
    app.run()
