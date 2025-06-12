import requests
from datetime import datetime, timedelta

def get_weather(location: str):
    try:
        # First, get coordinates for the location
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_resp = requests.get(geocoding_url, timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data.get('results'):
            return None

        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        location_name = geo_data['results'][0]['name']

        # Then get weather data for those coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        weather_resp = requests.get(weather_url, timeout=10)
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        # Weather code to description mapping
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }

        current = weather_data['current']
        weather_code = current['weather_code']
        weather_desc = weather_codes.get(weather_code, "Unknown")

        return {
            "location": location_name,
            "description": weather_desc,
            "temperature_C": current['temperature_2m'],
            "humidity_%": current['relative_humidity_2m'],
            "wind_speed_m/s": current['wind_speed_10m']
        }
    except Exception as e:
        return None

def get_historical_weather(location: str, days: int = 7):
    try:
        # Get coordinates
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_resp = requests.get(geocoding_url, timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data.get('results'):
            return None

        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']

        # Get historical data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&start_date={start_date.strftime('%Y-%m-%d')}"
            f"&end_date={end_date.strftime('%Y-%m-%d')}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"
        )

        weather_resp = requests.get(weather_url, timeout=10)
        weather_resp.raise_for_status()
        return weather_resp.json()
    except Exception as e:
        return None

def get_air_quality(location: str, airvisual_api_key: str):
    try:
        # First, get coordinates for the location
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_resp = requests.get(geocoding_url, timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data.get('results'):
            return None

        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']

        # Try Open-Meteo API first
        aq_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5,ozone,nitrogen_dioxide,sulphur_dioxide"
        aq_resp = requests.get(aq_url, timeout=10)

        if aq_resp.status_code == 200:
            aq_data = aq_resp.json()
            if 'current' in aq_data:
                return aq_data

        # If Open-Meteo fails, try AirVisual API
        airvisual_url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={airvisual_api_key}"
        airvisual_resp = requests.get(airvisual_url, timeout=10)

        if airvisual_resp.status_code == 200:
            airvisual_data = airvisual_resp.json()
            if 'data' in airvisual_data and 'current' in airvisual_data['data']:
                current = airvisual_data['data']['current']['pollution']
                return {
                    'current': {
                        'pm10': current.get('p1'),
                        'pm2_5': current.get('p2'),
                        'ozone': current.get('o3'),
                        'nitrogen_dioxide': None,
                        'sulphur_dioxide': None
                    }
                }

        return None
    except Exception as e:
        print(f"Air quality error: {str(e)}")
        return None 
