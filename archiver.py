import requests
import json

### Archives playlists into csv

## TODO: MAKE FUNCTION FOR AUTH
with open('../.auth/spotify.json') as f:
    config = json.load(f)
    
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1'
auth_response = requests.post(AUTH_URL, {'grant_type': 'client_credentials',
        'client_id': config['public_key'],
        'client_secret': config['secret_key']})

d = auth_response.json()
token = d['access_token']

headers = {'Authorization' : f'Bearer {token}'}

### BEGIN SCRAPE
MELLOWS_URI = '0FSKmSfycFXdvlJlsbHCJP'
end = False
offset = 0
table = {'name':[], 'artist(s)':[], 'album':[], 'added by':[], 'added at':[]}
while not end:
    r = requests.get(f'{BASE_URL}/playlists/{MELLOWS_URI}/tracks?&offset={offset}', headers=headers).json()
    tracks = r['items']
    for s in tracks:
        song = s['track']
        table['name'].append(song['name'])
        artists = song['artists']
        if isinstance(artists, list): #multiple artists case
            artist_names = ''
            for a in artists:
                artist_names += f'{a["name"]}, '
            table['artist(s)'].append(artist_names[:-2]) #remove trailing comma
        else:
            table['artist(s)'].append(artists['name'])
        table['album'].append(song['album']['name'])
        table['added by'].append(s['added_by']['id'])
        table['added at'].append(s['added_at'])
    if len(tracks) == 0:
        end = True
        print(f'collected {r["total"]} songs')
    offset += 100
    
import pandas as pd
archive = pd.DataFrame(table)
# archive.to_csv()