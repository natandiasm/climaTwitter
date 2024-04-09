from datetime import datetime


# Get the information coming from openweathermap about the current weather and format it to text
def format_text_current_weather(current_weather: dict) -> str:
    current_date_weather = datetime.fromtimestamp(current_weather['dt'])
    current_formated_data = f"{current_date_weather.day}/{current_date_weather.month}"
    current_temp = current_weather['main']['temp']
    current_description = current_weather['weather'][0]['description']
    current_city = current_weather['name']
    return f"{current_temp}°C e {current_description} em {current_city} em {current_formated_data}"


def format_text_forecast(forecast: dict) -> str:
    days = {}
    next_days = []

    # get average temp in days
    for day in forecast['list']:
        date_day = datetime.fromtimestamp(day['dt'])
        day_formated = f'{date_day.day}/{date_day.month}'
        temp = day['main']['temp']

        if day_formated in days:
            old_temp = days[day_formated]
            day[day_formated] = (temp + old_temp) / 2
        else:
            days[day_formated] = temp

    # formated text days to post
    for day in days:
        next_days.append(f"{days[day]}°C em {day}")

    formeted_days = ', '.join(next_days)

    formeted_forecast_text = f"Média para os próximos dias: {formeted_days}."

    return formeted_forecast_text
