import requests
import pandas as pd
from datetime import datetime, timedelta
from .risk_analysis import calculate_risk_level, calculate_time_ago, categorize_magnitude, categorize_depth


def fetch_earthquakes(min_magnitude=2.5, hours=24, region_bbox=None):
    try:
        endtime = datetime.utcnow()
        starttime = endtime - timedelta(hours=hours)

        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {
            "format": "geojson",
            "starttime": starttime.strftime('%Y-%m-%dT%H:%M:%S'),
            "endtime": endtime.strftime('%Y-%m-%dT%H:%M:%S'),
            "minmagnitude": min_magnitude,
            "orderby": "time"
        }

        if region_bbox:
            params.update({
                "minlatitude": region_bbox[1],
                "maxlatitude": region_bbox[3],
                "minlongitude": region_bbox[0],
                "maxlongitude": region_bbox[2]
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
                'url': prop['url']
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

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()
