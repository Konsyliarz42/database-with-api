from marshmallow import Schema, fields, post_load
from uuid import uuid4

#================================================================
class Song():
    def __init__(self, band_name, album_name, nr, title):
        self.band_name  = band_name
        self.album_name = album_name
        self.nr         = nr
        self.title      = title
        self.song_id    = str(uuid4())


    @property
    def _links(self):
        return {
            'self': f"http://localhost:5000/songs/{self.song_id}",
            'collection': "http://localhost:5000/songs"
        }

    #--------------------------------
    def __repr__(self):
        return f"{self.band_name} - {self.title}"

    #--------------------------------
    def __eq__(self, other):
        return all((
            self.band_name  == other.band_name,
            self.album_name == other.album_name,
            self.nr         == other.nr,
            self.title      == other.title
        ))

#================================================================
class SongSchema(Schema):
    band_name   = fields.String(required=True)
    album_name  = fields.String(required=True)
    nr          = fields.Integer(required=True)
    title       = fields.String(required=True)
    song_id     = fields.UUID()
    _links      = fields.Dict()

    @post_load
    def make_song(self, data, **kwargs):
        return Song(**data)