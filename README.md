# weatherAPI

This program uses Flask to create a service that, given a city name, collects data from the ​Open Weather API​, caches it for some time, and returns it as a JSON object. Also returns a configurable number of the last searched cities present in cache.

## Dependencies

This API uses **Python 3.6+**, **Flask** and **flask-cache**.

## How to run

As long as you have the dependencies, you can run the Python script. You should also go to https://openweathermap.org/current to get your OpenWeather API key and input it to the API_KEY configuration variable in index_API.py

> **> python index_API.py**

It's also possible to run the app by calling flask directly but its necessary to set the environment variable FLASK_APP first:

> **> set FLASK_APP=index_API**\
> **> flask run**\
> **Running on http://127.0.0.1:5000/**

It will create a local server that can be accessed by http://127.0.0.1:5000/ or http://localhost:5000/ and the API call can be done using the following paths:

|               PATH          |METHOD |DESCRIPTION                                                                       |
|-----------------------------|-------|----------------------------------------------------------------------------------|
|/weather?max=**​<max_number>**|GET    |Get all the cached cities, up to the latest 5 entries (configurable in code), or **​max_number​** ​ (if specified)​             |
|/weather/​**<city_name>**     |GET    |Get the cache data for the specified **city_name​**, otherwise fetches from the Open Weather API, caches and returns the results.            |
