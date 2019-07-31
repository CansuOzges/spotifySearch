from django.shortcuts import render
from django.http import HttpResponse
import random, json, requests, base64
from django.template import loader

"""
Spotfiy client id and secret for development purposes.
"""
client_id = ""
client_secret = ""

"""
read genre.json file and load as json
"""
genre_artist =[]
with open('genres.json', 'r') as jfile:
	genre_artist = json.load(jfile)

def spotifySearch(request,genre):
	"""
	tracks/{genre} url's function, Retuns top 10 tracks of an artist as json.
	Args:
	    genre(str): music genre
	Returns:
        HttpRespons: Returns json if it's exist. Otherwise returns a warning.
    Example:
        spotifySearch("rock")
        >	[
			  {
				"album_image_url": "https://i.scdn.co/image/26098aaa50a3450f0bac8f1a7d7677accf3f3cb6",
				"preview_url": "https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=f9d9e68e68194c5a90c56ef00c77eb1f",
				"track": "Uprising",
				"artist": "Muse"
				}
  			]
	"""
	if genre in genre_artist.keys():
		tracks = top_tracks(genre)
		if tracks:
			return HttpResponse(json.dumps(tracks))
		else:
			response ={"message":"Artist/track is not found.", "error":True}
			return HttpResponse(json.dumps(response))
	else:
		response = {"message": "Please give an existed genre as a parameter. Genres are: rock, alternative rock, pop, blues, country, electronic, jazz, r&b, rap, reggae.", "error":True}
		return HttpResponse(json.dumps(response))

def mainPage(request):
	"""
	Main page. First it reloads main.html. If user gives a genre it reloads result.html.

	Returns:
	    HttpResponse: Returns main.html for search and result.hmtl for search reasult. Returns main.html if result is empty.
	"""
	data = request.POST.copy()
	genre = data.get('genre')
	html_data = None

	if genre:
		if genre in genre_artist.keys():
			html_data = top_tracks(genre)
			template = loader.get_template('result.html')
		else:
			html_data = {'message': 'Please give an existed genre as a parameter. Genres are: rock, alternative rock, pop, blues, country, electronic, jazz, r&b, rap, reggae.'}
			template = loader.get_template('main.html')
	else:
		template = loader.get_template('main.html')

	context = {
		'tracks': html_data,
	}
	return HttpResponse(template.render(context, request))

def get_token():
	"""
	Get spotify token for authorization with using client_id and secret which are encoded to base64. Returns token.

	Args:
	    None
	Returns:
	    string: If token is created returns token as str. Otherwise it returns none.
	Example:
	    get_token()
	    >BQsad35482
	"""
	headers = {
		'Authorization': 'Basic ' + (base64.b64encode((client_id + ':' + client_secret).encode("utf-8"))).decode("utf-8")}
	options = {
		'grant_type': 'client_credentials',
		'json': True,
	}

	response = requests.post(
		'https://accounts.spotify.com/api/token',
		headers=headers,
		data=options
	)
	if response.status_code == 200:
		content = json.loads(response.content.decode('utf-8'))
		access_token = content.get('access_token', None)
		return access_token
	else:
		return None


def search_for_artist(name):
	"""
	Spotify search for artist. This returns only the one element. Query is limited to one. After query result, it returns artist id.
	Args:
	    name(str): Artist's name or band.
	Returns:
	    string: Returns artist's id if it's found. Otherwise returns None.
	Example:
	    search_for_artist("Muse")
	    >12dhd87264653
	"""
	token = get_token()
	if token:
		headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
		options = {
			'q': name, 'type': 'artist', 'limit': '1'
		}

		response = requests.get(
			'https://api.spotify.com/v1/search',
			headers=headers,
			params=options
		)
		if response.status_code == 200:
			content = json.loads(response.content.decode('utf-8'))
			if content:
				return content['artists']['items'][0]['id']
			else: return None
		else:
			return None
	else:
		return None

def search_for_artist_top_tracks(name):
	"""
	Spotifty artist's top track function. Spotify's query returns only 10 elements as json. Query takes artist id.
	Args:
	    name(str): Artist's name or band.
	Returns:
	    json:Returns top 10 tracks as json if they're found. Otherwise returns None.
	Example:
	    search_for_artist_top_tracks("Muse"):
	    > [
			  {
				"album_image_url": "https://i.scdn.co/image/26098aaa50a3450f0bac8f1a7d7677accf3f3cb6",
				"preview_url": "https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=f9d9e68e68194c5a90c56ef00c77eb1f",
				"track": "Uprising",
				"artist": "Muse"
			  }
		]
	"""
	artist_id = search_for_artist(name)
	token = get_token()
	if artist_id and token:
		headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
		options = {'country': 'TR'}
		response = requests.get(
			'https://api.spotify.com/v1/artists/'+artist_id+'/top-tracks',
			headers=headers,
			params=options
		)
		if response.status_code == 200:
			content = json.loads(response.content.decode('utf-8'))
			if content:
				return content['tracks']
			else: return None
		else:
			return None
	else:
		return None

def top_tracks(genre):
	"""
	After getting the top tracks, it formats the json as a new one. It takes only wanted attributes of json.

	Args:
	    genre(str):music genre
	Returns:
	    json: It returns json if top tracks are found. Otherwise it returns None.
	Example:
	    top_tracks("rock")
	    >[
		  {
			"album_image_url": "https://i.scdn.co/image/26098aaa50a3450f0bac8f1a7d7677accf3f3cb6",
			"preview_url": "https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=f9d9e68e68194c5a90c56ef00c77eb1f",
			"track": "Uprising",
			"artist": "Muse"
		  }
		]
	"""
	artist = random.choice(genre_artist[genre])
	top_tracks = search_for_artist_top_tracks(artist)
	items = []
	if top_tracks:
		for track in top_tracks:
			items.append({"artist": track["artists"][0]["name"], "popularity": track["popularity"], "track": track["name"],
				 "preview_url": track["preview_url"], "album_image_url": track["album"]["images"][2]["url"]})
		items = sorted(items, key=lambda x: x['popularity'], reverse=True)
		for item in items:
			del item['popularity']
		return items
	else:
		return None
