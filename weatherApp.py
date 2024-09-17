import requests

# API keys
API_KEY = 'YOUR_API_KEY_HERE' # placeholder
BASE_URL_WEATHER = "http://api.openweathermap.org/data/2.5/weather?"
IP_INFO_URL = "http://ipinfo.io"

# Function to get current weather by city name
def get_current_weather(city_name, units):
    complete_url = f"{BASE_URL_WEATHER}q={city_name}&appid={API_KEY}&units={units}"

    try:
        response = requests.get(complete_url, timeout=5)  # Add timeout
        response.raise_for_status()  # Raise exception for 4xx and 5xx errors
        data = response.json()

        if data["cod"] != "404":
            # Extracting data
            main = data["main"]
            wind = data["wind"]
            weather_description = data["weather"][0]["description"]

            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]

            # Store info in dictionary
            weather_info = {
                "city": city_name.capitalize(),
                "temperature": temperature,
                "description": weather_description.capitalize(),
                "humidity": humidity,
                "pressure": pressure,
                "wind_speed": wind_speed,
                "units": units
            }

            return weather_info
        else:
            print(f"City '{city_name}' not found. Please check the spelling and try again.\n")
            return None

    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except requests.exceptions.ConnectionError: # Handle connection errors
        print("There was a connection error. Please check your internet connection.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

# Function to get weather by coordinates
def get_weather_by_coordinates(lat, lon, units):
    complete_url = f"{BASE_URL_WEATHER}lat={lat}&lon={lon}&appid={API_KEY}&units={units}"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        wind = data["wind"]
        weather_description = data["weather"][0]["description"]

        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        wind_speed = wind["speed"]

        weather_info = {
            "city": data["name"],
            "temperature": temperature,
            "description": weather_description.capitalize(),
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "units": units
        }

        return weather_info
    else:
        print("Weather data for the location not found.")
        return None

# Function to get user's current location based on IP
def get_current_location():
    response = requests.get(IP_INFO_URL)
    data = response.json()
    loc = data["loc"]  # Get latitude and lon
    lat, lon = loc.split(',')
    return lat, lon

# Function to print weather info
def print_weather_info(weather_info, units):
    unit_temp = 'C' if units == 'metric' else 'F'
    unit_wind = 'm/s' if units == 'metric' else 'mph'
    
    print("\n" + "-"*33)
    print(f"Current Weather in {weather_info['city']}:\n")
    print(f"Temperature: {weather_info['temperature']}°{unit_temp}")
    print(f"Weather Description: {weather_info['description']}")
    print(f"Humidity: {weather_info['humidity']}%")
    print(f"Pressure: {weather_info['pressure']} hPa")
    print(f"Wind Speed: {weather_info['wind_speed']} {unit_wind}")
    print("-"*33)

# Function to compare weather between two cities (or same city with different units)
def compare_weather(city1, city2, units):
    weather1 = get_current_weather(city1, units)
    if city1 == city2:  # If user wants to compare the same city, switch the units
        toggle_units = "imperial" if units == "metric" else "metric"
        weather2 = get_current_weather(city2, toggle_units)
        unit_compare = True
    else:
        weather2 = get_current_weather(city2, units)
        unit_compare = False

    if weather1 and weather2:
        unit_temp = 'C' if units == 'metric' else 'F'
        unit_wind = 'm/s' if units == 'metric' else 'mph'
        toggle_temp = 'F' if units == 'metric' else 'C'
        toggle_wind = 'mph' if units == 'metric' else 'm/s'

        # Print comparison
        if unit_compare:
            print("\n" + "-" * 52)
            print(f"Weather Comparison for {weather1['city']} (Metric vs Imperial):\n")
            print(f"Temperature: {weather1['temperature']}°{unit_temp} vs {weather2['temperature']}°{toggle_temp}")
            print(f"Sky Clarity: {weather1['description']}")
            print(f"Humidity: {weather1['humidity']}%")
            print(f"Pressure: {weather1['pressure']} hPa")
            print(f"Wind Speed: {weather1['wind_speed']} {unit_wind} vs {weather2['wind_speed']} {toggle_wind}")
            print("-" * 52)
        else:
            print("\n" + "-" * 40)
            print(f"Weather Comparison: {weather1['city']} vs {weather2['city']}:\n")
            print(f"Temperature: {weather1['temperature']}°{unit_temp} vs {weather2['temperature']}°{unit_temp}")
            print(f"Sky Clarity: {weather1['description']} vs {weather2['description']}")
            print(f"Humidity: {weather1['humidity']}% vs {weather2['humidity']}%")
            print(f"Pressure: {weather1['pressure']} hPa vs {weather2['pressure']} hPa")
            print(f"Wind Speed: {weather1['wind_speed']} {unit_wind} vs {weather2['wind_speed']} {unit_wind}")
            print("-" * 40)
    else:
        # If one or both cities are not found
        print("Unable to compare the cities due to missing data.\n")

def main():
    print("Welcome to the Weather App!")
    
    # Default unit is metric
    units = "metric"

    while True:
        print("\n1. Get Current Weather by City")
        print("2. Get Current Weather by Location")
        print("3. Compare Weather between Two Cities")
        print("4. Toggle Units (Metric/Imperial)")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            city_name = input("Enter the name of the city: ").strip()
            weather = get_current_weather(city_name, units)
            if weather:
                print_weather_info(weather, units)

        elif choice == "2":  # Fetch weather based on current location
            lat, lon = get_current_location()
            weather = get_weather_by_coordinates(lat, lon, units)
            if weather:
                print_weather_info(weather, units)

        elif choice == "3":
            city1 = input("Enter the first city: ").strip()
            city2 = input("Enter the second city: ").strip()
            compare_weather(city1, city2, units)

        elif choice == "4":  # Toggle units
            if units == "metric":
                units = "imperial"
                print("Switched to Imperial (°F, mph).")
            else:
                units = "metric"
                print("Switched to Metric (°C, m/s).")

        elif choice == "5":
            print("Exiting the weather app. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
