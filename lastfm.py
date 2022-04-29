import requests
import json
import requests_cache 
import numpy as np
import os
import datetime
import time

def clear():
	os.system("cls" if os.name == "nt" else "clear")

# Cache to avoid spamming API
requests_cache.install_cache()

API_KEY = 'Insert API Key here'
SECRET = 'Insert SECRET'
USER_AGENT = 'Insert USER AGENT'

# Function to get data from a specific album
def lastfm_get(payload):
	headers = {'user-agent': USER_AGENT}
	url = 'https://ws.audioscrobbler.com/2.0/'

	payload['api_key'] = API_KEY
	payload['artist'] = artist
	payload['album'] = album
	payload['autocorrect'] = '1'
	payload['format'] = 'json'

	response = requests.get(url, headers = headers, params = payload)
	return response

def jprint(obj):
	text = json.dumps(obj, sort_keys = True, indent = 4)
	print(text)

# Get all tracks from supplied album 
def get_album_tracks():

	r = lastfm_get({
	'method': 'album.getInfo'
	})

	album_tracks = (r.json()["album"]["tracks"]["track"])
	
	# String cleaning to remove extraneous content
	tracks_strings = str(album_tracks)
	tracks_strings = tracks_strings.replace('{', '')
	tracks_strings = tracks_strings.replace('}', '')
	album_tracks = tracks_strings.rsplit(", '")

	tracks_with_tag = []
	for i in album_tracks:
		if "name" in i:
			tracks_with_tag.append(i)

	tracks = []
	def artist_tag_remove():
		
		for i in tracks_with_tag:
			try:
				if artist in i:
					pass
				
				else:
					tracks.append(i)

			except IndexError:
				pass

	artist_tag_remove()

	# Get rid of more unwanted metadata
	nearly_final_tracks = []

	for i in tracks:
		if '"' in i:
			y = tracks.index(i)
			i = i.replace("name': ", '')
			i = i.replace('"', '')
			i = i.replace("'", '\'')
			nearly_final_tracks.insert(y, i)

		else:	
			i = i.replace('"', '')
			i = i.replace("name': ", '')
			i = i.replace("'':", '')
			i = i.replace("'", '')
			nearly_final_tracks.append(i)

	final_tracks = []
	for i in nearly_final_tracks:
		j = i.lstrip()
		final_tracks.append(j)

	get_track_info(final_tracks)

# Collect playcount for all songs on album
def get_track_info(final_tracks):
	playcounts = []
	length = np.arange(0, len(final_tracks), 1)
	print('Getting album data...')
	for i in length:
		track = final_tracks[i]

		def lastfm_get(payload):
			headers = {'user-agent': USER_AGENT}
			url = 'https://ws.audioscrobbler.com/2.0/'

			payload['api_key'] = API_KEY
			payload['artist'] = artist
			payload['track'] = track
			payload['autocorrect'] = '1'
			payload['format'] = 'json'
			time.sleep(0.333)
			response = requests.get(url, headers = headers, params = payload)
			return response

		r = lastfm_get({
			'method': 'track.getInfo'
			})

		try:
			number = r.json()['track']['playcount']
			playcounts.append(number)
		except KeyError:
			pass

	final_playcounts = []
	for i in playcounts:
		i = int(i)
		final_playcounts.append(i)
	data_save(final_tracks, final_playcounts, album, artist)
	
# Take input from text
def readFile(indexNo):
	
	# Set input file to read from below
	fileAlbums = open('alltimealbums.txt', "r")
	text_input = fileAlbums.read().rsplit('\n')
	count = len(text_input)
	nth_album = text_input[indexNo]
	fileAlbums.close()
	global artist, album
	artist, album = nth_album.split('§')
	try:
		get_album_tracks()
	except KeyError:
		pass
	
	if indexNo < count - 1:
		indexNo += 1
		readFile(indexNo)
	
	elif indexNo == count:
		menu() 

# Write to txt file
def data_save(final_tracks, final_playcounts, album, artist):

	album_data = [list(i) for i in zip(final_tracks, final_playcounts)]
	file = open('outputalltimeweek11.txt', 'a')
	for i in album_data:
		print(i)

	file.write('\n')
	file.write(artist + ',' + album)
	file.write('\n')
	file.write(str(album_data))
	file.close()

# Date Stamp	
def date_stamp():
	file = open('outputalltimeweek11.txt', 'a')
	generation_date = 'Generated %s' % datetime.datetime.now()
	file.write(generation_date)
	file.close()

# Basic UI
def menu():

	clear()

	print(" 1. Album Tracks\n 2. File Input\n 0. Exit")

	while True:
		try:
			print()
			choice = int(input("Enter choice: "))
			break
		except ValueError:
			print()
			print("Numbers only please!")

	if choice == 1:
		clear()
		global artist, album
		artist, album = input('Please enter the name of an artist, followed by an album by them, using § as a seperator: ').split('§')
		get_album_tracks()
	elif choice == 2:
		date_stamp()
		readFile(0)
		
	elif choice == 0:
		clear()
		exit()
	else:
		menu()

if __name__ == '__main__':
	menu()

