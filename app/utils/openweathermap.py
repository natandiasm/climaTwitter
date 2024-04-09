import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Get Weather of the cites
class OpenWeatherMap:
    _shared_state = {}
    _api_key = ""
    url_base = "https://api.openweathermap.org"

    def __new__(cls):
        inst = super().__new__(cls)
        inst.__dict__ = cls._shared_state
        return inst

    def start(self):
        self._api_key = os.getenv("OPENWEATHERMAP_KEY")

    def _make_request(self, url: str, query_params: dict) -> dict:
        response = requests.get(url, params=query_params)
        status_code = response.status_code

        if status_code == 200:
            data = response.json()
            if data:
                return data
            else:
                raise ValueError("OpenWeatherMap data not found")
        elif status_code == 401:
            raise ValueError("OpenWeatherMap key invalid")
        else:
            raise ValueError("OpenWeatherMap error on request")

    def current_weather(self, lat: float, lon: float) -> dict:
        url = f'{self.url_base}/data/2.5/weather'

        query_params = {
            "appid": self._api_key,
            "lat": lat,
            "lon": lon,
            "lang": 'pt_br',
            "units": 'metric'
        }

        return self._make_request(url, query_params)

    def forecast_daily(self, lat: float, lon: float) -> dict:
        url = f'{self.url_base}/data/2.5/forecast'

        query_params = {
            "appid": self._api_key,
            "lat": lat,
            "lon": lon,
            "lang": 'pt_br',
            "units": 'metric'
        }

        return self._make_request(url, query_params)

    def direct_geocoding(self, city_name: str) -> dict:
        url = f'{self.url_base}/geo/1.0/direct'
        query_params = {
            "q": f"{city_name},BR",
            "limit": 1,
            "appid": self._api_key
        }

        return self._make_request(url, query_params)