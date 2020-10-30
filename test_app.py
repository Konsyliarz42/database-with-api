import unittest, requests, random

session = requests.Session()
local   = 'http://127.0.0.1:5000/songs'

def add_to_session():
    bands   =   ["Ne Obliviscaris"]
    albums  =   ["Portal Of I", "Citadel", "Urn"]
    songs   =   [
                    ["Tapestry of the Starless Abstract","Xenoflux","Of the Leper Butterflies","Forget Not","And Plague Flowers the Kaleidoscope","As Icicles Fall","Of Petrichor Weaves Black Noise"],
                    ["Painters of the Tempest(Part I): Wyrmholes","Painters of the Tempest(Part II): Triptych Lux","Painters of the Tempest(Part III): Reveries from the Stained Glass Womb","Pyrrhic","Devour Me, Colossus(Part I): Blackholes","Devour Me, Colossus(Part II): Contortions"],
                    ["Libera(Part I): Saturnine Spheres","Libera(Part II): Ascent of Burning Moths","Intra Venus","Eyrie","Urn(Part I): And Within the Void We Are Breathless","Urn(Part II): As Embers Dance in Our Eyes"]
                ]

    for band in bands:
        for album in albums:
            for title in songs[albums.index(album)]:
                nr = songs[albums.index(album)].index(title) + 1
                session.post(   local,
                                json={  'band_name':    band,
                                        'album_name':   album,
                                        'nr':           nr,
                                        'title':        title   }
                            )

#================================================================
class TestGetResponse(unittest.TestCase):
    def test_get_all_songs(self):
        response = requests.get(local)

        assert response.status_code == 200


    def test_get_song_by_id(self):
        song_id     = requests.get(local).json()[random.randint(0, len(requests.get(local).json()) - 1)]['song_id']
        response    = requests.get(f"{local}/{song_id}")

        assert response.status_code == 200

    #----------------------------
    def test_post_song_first_time(self):
        song = {    'band_name':    'Nachtblut',
                    'album_name':   'Vanitas',
                    'nr':           4,
                    'title':        "Das Puppenhaus"    }

        response = requests.post(local, json=song)

        assert response.status_code == 201


    def test_post_song_second_time(self):
        song = {    'band_name':    'Nachtblut',
                    'album_name':   'Vanitas',
                    'nr':           4,
                    'title':        "Das Puppenhaus"   }

        response = requests.post(local, json=song)

        assert response.status_code == 409

    
    def test_post_song_bad_request(self):
        song = {    'band_name':    'Nachtblut',
                    'album_name':   'Vanitas',
                    'title':        "Das Puppenhaus"   }

        response = requests.post(local, json=song)

        assert response.status_code == 400


    def test_post_song_bad_request2(self):
        song = {    'band_name':    'Nachtblut',
                    'album_name':   'Vanitas',
                    'nr':           'x',
                    'title':        "Das Puppenhaus"   }

        response = requests.post(local, json=song)

        assert response.status_code == 400

    #----------------------------
    def test_put_song(self):
        song_id         = requests.get(local).json()[len(requests.get(local).json()) - 1]['song_id']
        modification    = { 'band_name':    'Nachtblut',
                            'album_name':   'Vanitas',
                            'nr':           2,
                            'title':        "Vanitas"  }

        response = requests.put(f"{local}/{song_id}", json=modification)

        assert response.status_code == 200


    def test_put_song_bad_request(self):
        song_id         = requests.get(local).json()[len(requests.get(local).json()) - 1]['song_id']
        modification    = { 'band_name':    'Nachtblut',
                            'album_name':   'Vanitas',
                            'title':        "Vanitas"  }

        response = requests.put(f"{local}/{song_id}", json=modification)

        assert response.status_code == 400


    def test_put_song_bad_request2(self):
        song_id         = requests.get(local).json()[len(requests.get(local).json()) - 1]['song_id']
        modification    = { 'band_name':    'Nachtblut',
                            'album_name':   'Vanitas',
                            'nr':           'x',
                            'title':        "Vanitas"  }

        response = requests.put(f"{local}/{song_id}", json=modification)

        assert response.status_code == 400

    #----------------------------
    def test_put_song_and_delete_song(self):
        song_id     = requests.get(local).json()[len(requests.get(local).json()) - 1]['song_id']
        response    = requests.delete(f"{local}/{song_id}")

        assert response.status_code == 200

#================================================================
if __name__ == '__main__':
    add_to_session()
    unittest.main()
