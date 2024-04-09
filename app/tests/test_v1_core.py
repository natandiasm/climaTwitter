import os
import random

from fastapi.testclient import TestClient

from app.main import app


def test_not_found_city():
    with TestClient(app) as client:
        response = client.post('/v1/tweet_weather/',
                               json={
                                   "city_name": "city not exists"
                               })
        assert response.status_code == 500
        assert response.json() == {
            "detail": [
                "OpenWeatherMap data not found"
            ]
        }


def test_post_tweet():
    cities = ['São Paulo', 'Rio de Janeiro', 'Salvador', 'Brasília', 'Fortaleza']
    with TestClient(app) as client:
        response = client.post('/v1/tweet_weather/',
                               json={
                                   "city_name": random.choice(cities)
                               })
        assert response.status_code == 200
        assert response.json() == {"posted": True}


def test_tweeter_key_error():
    os.environ["TWITTER_API_ACCESS_TOKEN"] = ""
    os.environ["TWITTER_API_ACCESS_TOKEN_SECRET"] = ""
    os.environ["TWITTER_API_CONSUMER_KEY"] = ""
    os.environ["TWITTER_API_CONSUMER_SECRET"] = ""
    with TestClient(app) as client:
        response = client.post('/v1/tweet_weather/',
                               json={
                                   "city_name": "patos"
                               })
        assert response.status_code == 500
        assert response.json() == {'detail': "Unable to tweet, reason:('401 Unauthorized\\nUnauthorized',)"}


def test_openweathermap_key_error():
    os.environ["OPENWEATHERMAP_KEY"] = ""
    with TestClient(app) as client:
        response = client.post('/v1/tweet_weather/',
                               json={
                                   "city_name": "patos"
                               })
        assert response.status_code == 500
        assert response.json() == {
            "detail": [
                "OpenWeatherMap key invalid"
            ]
        }
