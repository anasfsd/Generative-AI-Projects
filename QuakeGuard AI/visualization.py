# viz.py — map & charts
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
import numpy as np




def create_advanced_map(df, region_bbox=None):
if df.empty:
return None
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=6, tiles='OpenStreetMap')
for _, row in df.iterrows():
if row['magnitude'] >= 6.0:
color = 'red'; radius=15
elif row['magnitude'] >= 5.0:
color = 'orange'; radius=12
elif row['magnitude'] >= 4.0:
color = 'yellow'; radius=10
else:
color = 'green'; radius=8
popup_content = (
f"<b>Magnitude {row['magnitude']}</b><br>"
f"Location: {row['place']}<br>"
f"Time: {row['time'].strftime('%Y-%m-%d %H:%M:%S')}<br>"
f"Depth: {row['depth']:.1f} km<br>"
f"<a href=\"{row['url']}\" target=\"_blank\">USGS Details</a>"
)
folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=radius,
popup=popup_content, color=color, fill=True, fillOpacity=0.7).add_to(m)
if region_bbox:
folium.Rectangle(bounds=[[region_bbox[1], region_bbox[0]], [region_bbox[3], region_bbox[2]]],
color='blue', weight=2, fillOpacity=0.1).add_to(m)
return m




def create_comprehensive_charts(df, analysis):
if df.empty:
return []
charts = []
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['time'], y=df['magnitude'], mode='markers',
marker=dict(size=df['magnitude'] * 2, color=df['magnitude'], colorscale='Reds', showscale=True),
name='Earthquakes'))
if len(df) >= 2:
try:
z = np.polyfit(range(len(df)), df['magnitude'], 1)
p = np.poly1d(z)
fig1.add_trace(go.Scatter(x=df['time'], y=p(range(len(df))), mode='lines', name='Trend', line=dict(dash='dash')))
except Exception:
pass
fig1.update_layout(title='Earthquake Magnitude Over Time with Trend', xaxis_title='Time', yaxis_title='Magnitude', height=400)
charts.append(fig1)


fig2 = px.histogram(df, x='magnitude', nbins=min(20, len(df)), title='Magnitude Distribution')
fig2.update_layout(height=400)
charts.append(fig2)


fig3 = px.scatter(df, x='depth', y='magnitude', color='magnitude', title=
