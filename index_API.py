from flask import Flask, request
import json

app = Flask(__name__)

# Root page
@app.route("/")
def home():
    return "Hello! this is just a root page"

# Get all the cached cities, up to the latest n entries (configurable) or ​max_number​ ​(if specified)​.
@app.route("/weather")
def city_weather_hist():
    max_number = request.args.get('max', default=5, type=int)  # number of cities passed as argument
    return f"Retuning the last {max_number} cached cities."

# Get the cache data for the specified ​city_name​, otherwise fetches from the Open Weather API, caches and returns the results.
@app.route("/weather/<city_name>")
def city_weather(city_name=""):
    return f"Fetching weather for city <b>{city_name}</b>"


if __name__ == "__main__":
    app.run()
