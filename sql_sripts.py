#================================================================
create = {
    'table_songs':"""
    -- songs table
    CREATE TABLE IF NOT EXISTS songs
    (
        id integer PRIMARY KEY,
        song_id integer,
        band text,
        album text,
        nr integer,
        title text
    );""",

    'song':"""
    INSERT INTO songs(song_id, band, album, nr, title)
        VALUES(?, ?, ?, ?, ?)""",
}

#================================================================
read = {
    'songs':"""
    SELECT * FROM songs""",

    'song_by_song_id':"""
    SELECT * FROM songs WHERE song_id=?""",
}

#================================================================
update = {
    
}

#================================================================
delete = {
    
}

#================================================================
if __name__ == "__main__":
    crud    = [create, read, update, delete]
    names   = ['create', 'read', 'update', 'delete']

    for operation, name in zip(crud, names):
        print(f"{name}:")

        for key in operation.keys():
            print(f"\t- {key}")