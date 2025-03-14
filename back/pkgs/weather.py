import argparse
import requests
import json
import datetime
import sys

# Parse command line arguments
parser = argparse.ArgumentParser(description='Get the current weather for a location')
parser.add_argument('-c', '--city', type=str, help='City name (default: auto-detect)')
parser.add_argument('-u', '--units', type=str, choices=['metric', 'imperial'], default='metric',
                    help='Units of measurement (metric or imperial, default: metric)')
parser.add_argument('-k', '--api-key', type=str, help='OpenWeatherMap API key (optional)')
parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed weather information')
args = parser.parse_args()

# API key for OpenWeatherMap (free tier)
# In a production environment, this should be stored securely, not hardcoded
API_KEY = args.api_key or "4c05ae5e0be9a8c5d0f2c6e2f3d0f3c5"  # This is a placeholder, not a real API key

def get_location():
    """Auto-detect user's location based on IP address"""
    try:
        response = requests.get('https://ipinfo.io/json')
        if response.status_code == 200:
            data = response.json()
            return data.get('city', '')
    except Exception as e:
        print(f"Error detecting location: {e}", file=sys.stderr)
    return ''

def get_weather(city, units='metric'):
    """Get weather data from OpenWeatherMap API"""
    if not city:
        print("Error: City not specified and auto-detection failed.", file=sys.stderr)
        sys.exit(1)
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("Error: Invalid API key. Please provide a valid OpenWeatherMap API key.", file=sys.stderr)
            sys.exit(1)
        elif response.status_code == 404:
            print(f"Error: City '{city}' not found.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Error: API returned status code {response.status_code}", file=sys.stderr)
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to weather service: {e}", file=sys.stderr)
        sys.exit(1)

def display_weather(weather_data, units, verbose=False):
    """Display weather information in a user-friendly format"""
    city = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    description = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    
    # Convert timestamp to readable date and time
    sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
    
    # Units display
    temp_unit = "°C" if units == 'metric' else "°F"
    speed_unit = "m/s" if units == 'metric' else "mph"
    
    # Basic display
    print(f"\nWeather for {city}, {country}")
    print(f"Temperature: {temp}{temp_unit} (Feels like: {feels_like}{temp_unit})")
    print(f"Conditions: {description.capitalize()}")
    
    # Verbose display
    if verbose:
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} {speed_unit}")
        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")

def main():
    city = args.city or get_location()
    weather_data = get_weather(city, args.units)
    display_weather(weather_data, args.units, args.verbose)

if __name__ == "__main__":
    main()