from datetime import datetime
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



@app.route('/album_insert', methods=['POST'])
def album_insert(): 
    # Inserting New Row Info into Albums Table 
    album_info = [request.form['title'], request.form['artist'], datetime.strptime(request.form['released'], '%Y-%m-%d')]
    album_row = Albums(title=album_info[0], artist=album_info[1], released=album_info[2])
    DB.session.add(album_row)
    DB.session.commit() 
    # Quering DB to display table and row count on HTML 
    albums = Albums.query.all()
    rows_count = Albums.query.count() 
    return render_template('album_insert.html', new_row_info=album_info, Albums = albums, Rows_count=rows_count)


@app.route('/edit_album', methods=['POST'])
def edit_album():
    if "album_id" in request.form:
        album_id = request.form["row_id"]
        album_info = Albums.query.filter_by(id=album_id).first()
        # Quering DB to display table and row count on HTML 
        albums = Albums.query.all()
        rows_count = Albums.query.count()
        return render_template('album_edit.html', Rows_count=rows_count, Albums = albums, album_info = album_info)
    else:
        # Requesting Changes
        id = request.form['row_id']
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
        


@app.route('/album_delete', methods=['POST'])
def album_delete():
    album_id = request.form["row_id"]
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



@app.route('/tracks', methods=['POST'])
def tracks():
    album_id = request.form["row_id"]
    album_info = Albums.query.filter_by(id=album_id).first()
    songs_count = Tracks.query.filter_by(album_id=album_id).count()
    songs = Tracks.query.filter_by(album_id=album_id)
    return render_template('tracks.html', Songs=songs, songs_count=songs_count, album_info=album_info)


@app.route('/song_insert', methods=['POST'])
def song_insert(): 
    album_id = request.form["album_id"]
    album_info = Albums.query.filter_by(id=album_id).first()
    # Inserting New Song Info into Tracks Table 
    song_row = Tracks(album_id=album_id, name=request.form['name'], genre=request.form['genre'], duration=str(request.form['mins'])+':'+str(request.form['secs'])) 
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
        genre = request.form['genre']
        duration = str(request.form['mins'])+':'+str(request.form['secs'])
        # Replacing Changed features
        song = Tracks.query.get(song_id)
        song.name = name
        song.genre = genre
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
    app.run()

