from flask_sqlalchemy import SQLAlchemy

# Create a DB Object
# opening up the db connection
DB = SQLAlchemy()

class Albums(DB.Model):
    '''Creates a Album Table with SQLAlchemy'''
    # id column schema
    id = DB.Column(DB.Integer, primary_key = True, autoincrement=True)
    # title column schema
    title = DB.Column(DB.String(30), nullable = False)
    # artist column schema
    artist = DB.Column(DB.String(30), nullable = False)
    # released column schema
    released = DB.Column(DB.Date, nullable = False)

    def __repr__(self):
        return f'<Album: {self.title}>'

class Tracks(DB.Model):
    '''Creates a Tracks Table with SQLAlchemy'''
    # id column schema
    id = DB.Column(DB.Integer, primary_key = True, autoincrement=True)
    # User Column schema
    album_id = DB.Column(DB.Integer, DB.ForeignKey('albums.id'), nullable=False)
    # name column schema
    name = DB.Column(DB.String(30), default="None")
    # artist column schema
    genre = DB.Column(DB.String(30), default="None")
    # genre column schema
    duration = DB.Column(DB.Integer, default="None")

    def __repr__(self):
        return f'<Track: {self.name}>'