from flask import Flask, abort
from flask_restx import Api, Resource, fields
from marshmallow import ValidationError
import json

from models import Song, SongSchema
from database import SQLiteDatabase

#================================================================
database_file   = "db_file.db"
database        = SQLiteDatabase(file=database_file)
app             = Flask(__name__)
api             = Api(app)

song_model = api.model('Song', {    'band_name':fields.String(required=True),
                                    'album_name':fields.String(required=True),
                                    'nr':fields.Integer(required=True),
                                    'title':fields.String(required=True)})
                      
database.connect()
database.create_table(
    table_name='songs',
    song_id='text', primary_key='song_id',
    band='text',
    album='text',
    nr='integer',
    title='text',
    _links='text'
)

songs = database.select_from_table('songs')
database.disconnect()

#--------------------------------
def find_song_in_database(*, song=False, song_id=None):
    if song:
        database.connect()
        result = database.select_from_table(
            table_name='songs',
            band=song.band_name,
            album=song.album_name,
            nr=song.nr,
            title=song.title
        )
        database.disconnect()

        return bool(result)

    if song_id:
        database.connect()
        result = database.select_from_table(
            table_name='songs',
            song_id=song_id
        )
        database.disconnect()

        if result:
            result  = result[0]
            song    = Song(
                band_name=result['band'],
                album_name=result['album'],
                nr=result['nr'],
                title=result['title']
            )
            song.song_id = song_id

            return song

    return False

#--------------------------------
@api.route('/songs')
class SongsAll(Resource):
    @api.response(200, 'Success - Songs are loaded')
    def get(self):
        database.connect()
        result = database.select_from_table(table_name='songs')
        database.disconnect()

        return result

    #--------------------------------
    @api.response(201, 'Created - Song is added to database')
    @api.response(400, 'Bad Request - Request is not complete or is incorrect')
    @api.response(409, 'Conflict - Song is already in database')
    @api.expect(song_model, validate=True)
    def post(self):
        try:
            result = SongSchema().load(api.payload)
        except ValidationError as error:
            return error.messages, 400

        if not find_song_in_database(song=result):
            database.connect()
            database.add_to_table(
                table_name='songs',
                song_id=result.song_id,
                band=result.band_name,
                album=result.album_name,
                nr=result.nr,
                title=result.title,
                #_links=json.dumps(result._links)
            )
            database.disconnect()

            return {'result': 'Song is added'}, 201
        else:
            return {'result': 'Song is already in database'}, 409

#--------------------------------
@api.route('/songs/<song_id>')
class SongsWithID(Resource):
    @api.response(200, 'Success - Song is loaded')
    @api.response(409, 'Conflict - Song is already in database')
    def get(self, song_id):
        schema  = SongSchema()
        song    = find_song_in_database(song_id=song_id)

        if song:
            result = schema.dump(song)
            return result
        else:
            return {'result': 'Song is not find in database'}, 404

    #--------------------------------
    @api.expect(song_model, validate=True)
    @api.response(200, 'Success - Song is modified')
    @api.response(400, 'Bad Request - Request is not complete or is incorrect')
    @api.response(440, 'Not Found - Song ID is not found')
    def put(self, song_id):
        schema  = SongSchema()
        song    = find_song_in_database(song_id=song_id)

        if not song:
            return {'result': 'Song is not found in database'}, 404
        else:
            try:
                result = schema.load(api.payload)
                result.song_id = song_id
            except ValidationError as error:
                return error.messages, 400

            database.connect()
            database.update_row(
                table_name='songs',
                primary_key={'name': 'song_id', 'value': song_id},
                band=result.band_name,
                album=result.album_name,
                nr=result.nr,
                title=result.title,
                #_links=json.dumps(result._links)
            )
            database.disconnect()

            return {'result': 'Song is modified'}

    #--------------------------------
    @api.response(200, 'Success - Song is removed')
    @api.response(440, 'Not Found - Song ID is not found')
    def delete(self, song_id):
        song = find_song_in_database(song_id=song_id)

        if song:
            database.connect()
            database.delete(
                table_name='songs',
                song_id=song_id
            )
            database.disconnect()
            
            return {'result': 'Song is removed'}
        else:
            abort(404)

#================================================================
if __name__ == "__main__":
    app.run(debug=True)