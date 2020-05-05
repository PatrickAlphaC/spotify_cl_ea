# coding: utf-8
import requests
import json
import os
import logging as log
import time
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

log.basicConfig(level=log.INFO)

_SPOTIFY_CLIENT_ID= os.getenv("SPOTIFY_CLIENT_ID")
_SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
# The above two are just for debugging
_API_URL_PREFIX = "https://www.alphavantage.co/query?function="
_API_URL_TOKEN_PREFIX = "https://accounts.spotify.com/api/token"
_RETRIES = 5


def lambda_handler(event, context):
    result = handler(event)
    return result


def gcs_handler(request):
    spotify_data = request.json
    result = handler(spotify_data)
    return json.dumps(result)


def handler(spotify_request_data):
    if 'data' not in spotify_request_data:
        spotify_request_data['data'] = {}
    if 'id' not in spotify_request_data:
        spotify_request_data['id'] = ""
    artist_data = spotify_request_data['data']
    log.info("Request data " + str(spotify_request_data['data']))

    json_response = handle_api_call(artist_data, _RETRIES)
    error_string = None

    if not json_response:
        error_string = 'Error getting data from the api, no return was given.'
        log.error(error_string)
    elif "error" in json_response:
        error_string = json_response["error"]
        

    adapter_result = {'jobRunID': spotify_request_data['id'],
                      'data': json_response}

    if error_string is not None:
        adapter_result['error'] = error_string
    return adapter_result


def handle_api_call(query_data, retries):
    try:
        json_response = None
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        json_response = sp.artist(query_data['artist'])
    except:
        e = sys.exc_info()[0]
        log.warning(
            "Retring with {} retries left, due to: {}".format(retries, e))
        log.warning("This was run with {}".format(query_data))
        if retries <= 0:
            sys.exit()
            return None
        time.sleep(0.1)
        return handle_api_call(query_data, retries - 1)

    if retries > 0:
        if not json_response:
            log.warning(
                "Retring with {} retries left, due to no response".format(retries))
            time.sleep(0.1)
            return handle_api_call(query_data, retries - 1)
        elif "error" in json_response:
            log.info(
                "Retring with {} retries left, due to Error message".format(retries))
            time.sleep(0.1)
            return handle_api_call(query_data, retries - 1)
    return json_response