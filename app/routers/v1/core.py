from fastapi import APIRouter, HTTPException

from app.models.tweet_weather import TweetWeather
from app.utils.format_text import format_text_current_weather, format_text_forecast
from app.utils.openweathermap import OpenWeatherMap
from app.utils.twitter import Twitter

router = APIRouter()


@router.post("/tweet_weather/", description="Tweet the current weather and the weather for the next 4 days.")
async def tweet_weather(twt_w: TweetWeather):
    # create instance OpenWeatherMap
    owm = OpenWeatherMap()
    # get info about city
    try:
        info_city = owm.direct_geocoding(twt_w.city_name)
    except ValueError as error:
        raise HTTPException(status_code=500, detail=error.args)
    # get lat,lon city
    city_lat = info_city[0]['lat']
    city_lon = info_city[0]['lon']
    # get current weather city
    try:
        current_weather = owm.current_weather(city_lat, city_lon)
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Weather information is not available for the city")
    # get forecast city
    try:
        forecast = owm.forecast_daily(city_lat, city_lon)
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Weather forecast information is not available for the city")
    # format info to make tweet
    current_weather_text = format_text_current_weather(current_weather)
    forecast_text = format_text_forecast(forecast)
    tweet_text = f"{current_weather_text}. {forecast_text}"

    twt = Twitter()
    try:
        twt.make_tweet(tweet_text)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Unable to tweet, reason:{error.args}")
    return {"posted": True}
