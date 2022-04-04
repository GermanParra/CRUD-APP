from ast import Return
from datetime import datetime
import sqlite3
from typing import Type
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
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    rows_count = Albums.query.count()
    
    return render_template('home.html', Albums = albums, Rows_count=rows_count)


@app.route('/album_insert', methods=['POST'])
def album_insert():
    album_info=[]
    if request.method == 'POST':
        # Inserting New Row Info into Albums Table 
        album_info = [request.form['title'], request.form['artist'], datetime.strptime(request.form['released'], '%Y-%m-%d')]
        row = Albums(title=album_info[0], artist=album_info[1], released=album_info[2])
        DB.session.add(row)
        DB.session.commit()

    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    rows_count = Albums.query.count()
    
    return render_template('insert.html', new_row_info=album_info, Albums = albums, Rows_count=rows_count)


@app.route('/reset', methods=['POST'])
def reset():
    # Reseting Database
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    rows_count = Albums.query.count()
    return render_template('reset.html', Albums = albums, Rows_count=rows_count)


@app.route('/edit', methods=['POST'])
def edit():
    if "row_id" in request.form:
        album_id = request.form["row_id"]
        album_info = Albums.query.filter_by(id=album_id).first()
        # Quering DB to display table and row count on HTML 
        albums = Albums.query.all()
        rows_count = Albums.query.count()
        return render_template('album_edit.html', Rows_count=rows_count, Albums = albums, album_info = album_info)
    else:
        # Requesting Changes
        id = request.form['album_id']
        title = request.form['edited_title']
        artist = request.form['edited_artist']
        released = request.form['edited_released']
        # Replacing Changed features
        row = Albums.query.get(id)
        row.title = title
        row.artist = artist
        row.released = datetime.strptime(released, '%Y-%m-%d')
        # Saving Changes
        DB.session.commit()
        # Quering DB to display table and row count on HTML 
        albums = Albums.query.all()
        rows_count = Albums.query.count()
    
        return render_template('home.html', Albums = albums, Rows_count=rows_count)
        

if __name__ == '__main__':
    app.run()

