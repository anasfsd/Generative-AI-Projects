import requests
from datetime import datetime, timedelta
import pandas as pd
from groq import Groq
from config import GROQ_API_KEY

def get_groq_summary(prompt, context=""):
    """Enhanced Groq LLM function with context and better error handling"""
    if not GROQ_API_KEY:
        return "API key not configured"
    try:
        client = Groq(api_key=GROQ_API_KEY)
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert seismologist, emergency response specialist, and public safety advisor. Provide detailed, accurate, and actionable information."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=2048,
            temperature=0.7,
            top_p=0.9,
            presence_penalty=0.1,
            frequency_penalty=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Analysis Error: {str(e)}"

def fetch_earthquakes(min_magnitude=2.5, hours=24, region_bbox=None, detailed=True):
    """Fetch earthquake data with enhanced error handling and data processing"""
    try:
        endtime = datetime.utcnow()
        starttime = endtime - timedelta(hours=hours)

        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "starttime": starttime.strftime('%Y-%m-%dT%H:%M:%S'),
            "endtime": endtime.strftime('%Y-%m-%dT%H:%M:%S'),
            "minmagnitude": min_magnitude,
            "orderby": "time",
            "limit": 500 if detailed else 200
        }

        if region_bbox:
            params.update({
                "minlatitude": region_bbox[1],
                "maxlatitude": region_bbox[3],
                "minlongitude": region_bbox[0],
                "maxlongitude": region_bbox[2],
            })

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        features = data.get('features', [])
        earthquakes = []

        for f in features:
            prop = f['properties']
            geom = f['geometry']

            earthquake = {
                'time': datetime.utcfromtimestamp(prop['time']/1000),
                'place': prop['place'],
                'magnitude': prop['mag'],
                'longitude': geom['coordinates'][0],
                'latitude': geom['coordinates'][1],
                'depth': geom['coordinates'][2],
                'url': prop['url'],
                'type': prop.get('type', 'earthquake'),
                'status': prop.get('status', 'automatic'),
                'tsunami': prop.get('tsunami', 0),
                'felt': prop.get('felt', 0),
                'cdi': prop.get('cdi', 0),
                'mmi': prop.get('mmi', 0),
                'alert': prop.get('alert', ''),
                'sig': prop.get('sig', 0)
            }

            earthquake['risk_level'] = calculate_risk_level(earthquake['magnitude'])
            earthquake['time_ago'] = calculate_time_ago(earthquake['time'])

            earthquakes.append(earthquake)

        df = pd.DataFrame(earthquakes)

        if not df.empty:
            df['magnitude_category'] = df['magnitude'].apply(categorize_magnitude)
            df['depth_category'] = df['depth'].apply(categorize_depth)
            df['hour_of_day'] = df['time'].dt.hour
            df['day_of_week'] = df['time'].dt.day_name()

        return df

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Data processing error: {e}")
        return pd.DataFrame()
