# Weather Forecast App

This is a command-line based weather forecast application that allows users to:

- Get current weather data by city name.
- Get weather based on the user's current geographical location (determined by IP address).
- Compare weather between two cities or between different units (Metric and Imperial).
- Switch between Metric and Imperial units.

The application uses the OpenWeatherMap API for weather data and IPInfo to determine the user's location.

## Features

### Get Weather by City Name:
- Users can input a city name and get the current temperature, weather description, humidity, pressure, and wind speed for that location.

### Get Weather by Location:
- Automatically retrieves the user's location using IPInfo and fetches the current weather for that location.

### Compare Weather Between Two Cities:
- Compare the weather between two cities or the same city in different units (Metric vs Imperial).

### Toggle Between Units:
- Users can toggle between Metric (Celsius, m/s) and Imperial (Fahrenheit, mph) units.

## API Keys

This project uses two external APIs:

- **OpenWeatherMap API**: To fetch weather data.
- **IPInfo API**: To fetch the user's current location.

**Note**: You will need to replace the placeholder `API_KEY` in the code with your actual OpenWeatherMap API key.

```python
API_KEY = 'YOUR_API_KEY_HERE'
```


## Prerequisites

- Python 3.x
- `requests` module

You can install the `requests` module using pip if you don't already have it:

```bash
pip install requests

