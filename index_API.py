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
    
    max_number = request.args.get('max', default=app.config['latestCitiesNum'])  # number of cities passed as argument
    weather_hist = {}

    try:
        if int(max_number) < 0 :
            raise ValueError

        if max_number > app.config["CACHE_SIZE"]:
            raise IndexError

        for city in search_history[0:max_number]:
            weather_hist[city] = cache.get(city)

    except ValueError:
        return "max provided is not a positive integer", 400
    except IndexError:
        return "I only have memory for the last 300 cached entries, please set an ask for max<=300.", 422 

    return json.dumps(weather_hist)

# Get the cache data for the specified ​city_name​, otherwise fetches from the Open Weather API, caches and returns the results.
@app.route("/weather/<city_name>")
def city_weather(city_name=""):
    response = cache.get(city_name.casefold())

    if response:
        return response

    # call OpenWeather API and save json response
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={app.config['API_KEY']}"

    response = requests.get(url).json()

    if response["cod"] !=200:
        return response

    cache.set(city_name.casefold(), response) # CACHE_DEFAULT_TIMEOUT is imported from app.config

    search_history.pop()
    search_history.insert(0,city_name.casefold())

    return response


if __name__ == "__main__":
    app.config.update(
        API_KEY = "acd04fdc6116982e7ee72c278537afef",           # OpenWeather API_KEY
        latestCitiesNum = 5,                                    # Number of cities to be returned by default
        CACHE_TYPE = "SimpleCache",                             # Flask-Caching related configs
        CACHE_DEFAULT_TIMEOUT = 300,                            # Cashe Timeout in seconds
        CACHE_SIZE = 300
    )

    search_history = ['']*app.config["CACHE_SIZE"]
    cache = Cache(app)
    app.run()
