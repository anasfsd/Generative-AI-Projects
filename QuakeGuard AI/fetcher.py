# fetcher.py — USGS data fetching
import requests
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional




def fetch_earthquakes(min_magnitude: float = 2.5, hours: int = 24, region_bbox: Optional[list] = None, detailed: bool = True) -> pd.DataFrame:
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
r = requests.get(url, params=params, timeout=30)
r.raise_for_status()
data = r.json()
features = data.get('features', [])
earthquakes = []
for f in features:
prop = f.get('properties', {})
geom = f.get('geometry', {})
coords = geom.get('coordinates', [None, None, None])
t_ms = prop.get('time')
t = datetime.utcfromtimestamp(t_ms/1000) if t_ms else None
earthquake = {
'time': t,
'place': prop.get('place', 'Unknown'),
'magnitude': prop.get('mag'),
'longitude': coords[0],
'latitude': coords[1],
'depth': coords[2],
'url': prop.get('url', ''),
'type': prop.get('type', 'earthquake'),
'status': prop.get('status', 'automatic'),
'tsunami': prop.get('tsunami', 0),
'felt': prop.get('felt', 0),
'cdi': prop.get('cdi', 0),
'mmi': prop.get('mmi', 0),
'alert': prop.get('alert', ''),
'sig': prop.get('sig', 0)
}
earthquakes.append(earthquake)
df = pd.DataFrame(earthquakes)
if not df.empty:
df['hour_of_day'] = df['time'].dt.hour
df['day_of_week'] = df['time'].dt.day_name()
return df
