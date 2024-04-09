from pydantic import BaseModel


class TweetWeather(BaseModel):
    city_name: str