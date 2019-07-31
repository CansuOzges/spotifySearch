# spotifySearch
Spotify search for a genre. Genres are: rock, alternative rock, pop, blues, country, electronic, jazz, r&b, rap, reggae. 

You can access ui by  http://IP_ADDR:PORT
In user interface there are a textbox and a button for search. You can type a genre and click the search button. App provides you a random artist for the genre. Artist is selected from genres.json file. When the artist is selected it will return top 10 tracks of the artist. Top 10 tracks will be sorted by popularity attribute.

You can access top 10 tracks as json by http://IP_ADDR:PORT/tracks/{genre}
Example:
http://localhost:8000/tracks/rock
[{"album_image_url": "https://i.scdn.co/image/f4f6903d134ff489abbc7ea5545c6cd3a5cb51df", "track": "All Along the Watchtower", "preview_url": "https://p.scdn.co/mp3-preview/5eec2933740ab3984340d5f004813f8275e1bb97?cid=f9d9e68e68194c5a90c56ef00c77eb1f", "artist": "Jimi Hendrix"},
.....
]

Libraries that been used in project:
--views.py--
random
json
requests
base64

Django 2.2.3 and Python 3 are used. 

!!!client_id and client_secret are empty.You can enter your client_id and secret in view.py. You can get it from spotfiy by creating an app.!!!
