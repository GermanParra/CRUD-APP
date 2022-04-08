from datetime import datetime
from distutils.log import debug
from flask import Flask, render_template, request #, redirect, url_for, jsonify
from models import DB, Albums, Tracks
import os
from spotify_data_access import search_albums, get_albums_data, get_albums_tracks_data, create_player_sources

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configurations
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Turn off verification when we request changes to db
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db' #getenv('DATABASE_URI')

# Connect DB to Flask app
DB.init_app(app)


@app.route('/')
def home():
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    albums_count = Albums.query.count()
    return render_template('home.html', Albums=albums, Albums_count=albums_count)


@app.route('/search', methods=['POST'])
def search():
    input_search = request.form['input_search']
    s_albums = search_albums(input_search)
    s_albums_data = get_albums_data(s_albums)
    s_albums_tracks_data = get_albums_tracks_data(s_albums_data)
    s_players = create_player_sources(s_albums_data)
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    albums_count = Albums.query.count()
    return render_template('home.html', Albums=albums, Albums_count=albums_count, S_albums_data=s_albums_data, S_tracks_data=s_albums_tracks_data, S_players=s_players)


@app.route('/album_insert', methods=['POST'])
def album_insert(): 
    # Inserting New Row Info into Albums Table 
    new_album = Albums(title=request.form['title'], artist=request.form['artist'], released=datetime.strptime(request.form['released'], '%Y-%m-%d'))
    DB.session.add(new_album)
    DB.session.commit() 
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    albums_count = Albums.query.count() 
    return render_template('album_insert.html', New_album=new_album, Albums=albums, Albums_count=albums_count)



@app.route('/edit_album', methods=['POST'])
def edit_album():
    if "editing_album_id" in request.form:
        editing_album = Albums.query.filter_by(id=request.form["editing_album_id"]).first()
        # Quering DB to display table and row count on HTML 
        albums = Albums.query.all()
        albums_count = Albums.query.count()
        return render_template('album_edit.html', Editing_album=editing_album, Albums=albums, Albums_count=albums_count)
    else:
        # Requesting Changes
        id = request.form['edited_album_id']
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
        albums_count = Albums.query.count() 
        return render_template('home.html',  Albums=albums, Albums_count=albums_count)
    
        

@app.route('/reset', methods=['POST'])
def reset():
    # Reseting Database
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    albums_count = Albums.query.count() 
    return render_template('reset.html', Albums=albums, Albums_count=albums_count)


@app.route('/tracks', methods=['POST'])
def tracks():
    album_id = request.form["exploring_album_id"]
    album_info = Albums.query.filter_by(id=album_id).first()
    # Quering DB to display song's table and count on HTML 
    songs_count = Tracks.query.filter_by(album_id=album_id).count()
    songs = Tracks.query.filter_by(album_id=album_id)
    return render_template('tracks.html', Songs=songs, songs_count=songs_count, album_info=album_info)



@app.route('/album_delete', methods=['POST'])
def album_delete():
    album_id = request.form["deleting_album_id"]
    album_info = Albums.query.filter_by(id=album_id).first()
    songs = Tracks.query.filter_by(album_id=album_id)
    DB.session.delete(album_info)
    for s in songs:
        DB.session.delete(s)       
    DB.session.commit()
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    rows_count = Albums.query.count()
    return render_template('album_delete.html', Albums=albums, Rows_count=rows_count, album_info=album_info)



@app.route('/song_insert', methods=['POST'])
def song_insert(): 
    album_id = request.form["album_id"]
    album_info = Albums.query.filter_by(id=album_id).first()
    # Inserting New Song Info into Tracks Table 
    song_row = Tracks(album_id=album_id, name=request.form['name'], duration=str(request.form['mins'])+':'+str(request.form['secs'])) 
    DB.session.add(song_row)
    DB.session.commit() 
    # Quering DB to display table and row count on HTML 
    songs_count = Tracks.query.filter_by(album_id=album_id).count()
    songs = Tracks.query.filter_by(album_id=album_id) 
    return render_template('tracks.html', Songs=songs, songs_count=songs_count, album_info=album_info)


@app.route('/edit_songs', methods=['POST'])
def edit_songs():
    if "album_id" in request.form:
        song_id = request.form['song_id']
        song_info = Tracks.query.filter_by(id=song_id).first()
        album_info = Albums.query.filter_by(id=song_info.album_id).first()
        # Quering DB to display table and row count on HTML 
        songs_count = Tracks.query.filter_by(album_id=song_info.album_id).count()
        songs = Tracks.query.filter_by(album_id=song_info.album_id) 
        return render_template('tracks_edit.html', Songs=songs, songs_count=songs_count, song_info = song_info, album_info=album_info)
    else:
        # Requesting Changes
        song_id = request.form['song_id']
        name = request.form['name']
        duration = str(request.form['mins'])+':'+str(request.form['secs'])
        # Replacing Changed features
        song = Tracks.query.get(song_id)
        song.name = name
        song.duration = duration
        # Saving Changes
        DB.session.commit()
        album_info = Albums.query.filter_by(id=song.album_id).first()
        # Quering DB to display table and row count on HTML 
        songs_count = Tracks.query.filter_by(album_id=song.album_id).count()
        songs = Tracks.query.filter_by(album_id=song.album_id) 
        return render_template('tracks.html', Songs=songs, songs_count=songs_count, album_info=album_info)


@app.route('/song_delete', methods=['POST'])
def song_delete():
    song_id = request.form["song_id"]
    song = Tracks.query.filter_by(id=song_id).first()
    album_id = song.album_id
    DB.session.delete(song)       
    DB.session.commit()

    album_info = Albums.query.filter_by(id=album_id).first()
    # Quering DB to display table and row count on HTML 
    songs_count = Tracks.query.filter_by(album_id=song.album_id).count()
    songs = Tracks.query.filter_by(album_id=song.album_id) 
    return render_template('tracks_delete.html', Songs=songs, songs_count=songs_count, album_info=album_info, song_info=song)







if __name__ == '__main__':
    app.run(debug=True)

