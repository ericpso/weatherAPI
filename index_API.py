from flask import Flask, request
from flask_caching import Cache
import requests
import json

app = Flask(__name__)

# Root page
@app.route("/")
def home():
    return "Hello! this is just the root page"

# Get all the cached cities, up to the latest n entries (configurable) or ​max_number​ ​(if specified)​.
@app.route("/weather")
def city_weather_hist():
    max_number = request.args.get('max', default=app.config['latestCitiesNum'], type=int)  # number of cities passed as argument
    return f"Retuning the last {max_number} cached cities."

# Get the cache data for the specified ​city_name​, otherwise fetches from the Open Weather API, caches and returns the results.
@app.route("/weather/<city_name>")
def city_weather(city_name=""):
    response = cache.get(city_name)

    if response:
        return f"Fetching weather for city <b>{city_name}</b> from cache. <p>{response}</p>"

    # call OpenWeather API and save json response
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={app.config['API_KEY']}"

    response = requests.get(url).json()
    cache.set(city_name, response) # CACHE_DEFAULT_TIMEOUT is imported from app.config

    return f"Fetching weather for city <b>{city_name}</b> <p>{response}</p>"


if __name__ == "__main__":
    app.config.update(
        API_KEY = "acd04fdc6116982e7ee72c278537afef",           # OpenWeather API_KEY
        latestCitiesNum = 5,                                    # Number of cities to be returned by default
        CACHE_TYPE = "SimpleCache",                             # Flask-Caching related configs
        CACHE_DEFAULT_TIMEOUT = 300                             # Cashe Timeout in seconds
    )

    cache = Cache(app)
    app.run()
