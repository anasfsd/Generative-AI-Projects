import folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from config import MAGNITUDE_COLORS

def create_advanced_map(df, region_bbox=None):
    """Create an advanced interactive map"""
    if df.empty:
        return None

    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles='OpenStreetMap'
    )

    for idx, row in df.iterrows():
        if row['magnitude'] >= 6.0:
            color = 'red'
            radius = 15
        elif row['magnitude'] >= 5.0:
            color = 'orange'
            radius = 12
        elif row['magnitude'] >= 4.0:
            color = 'yellow'
            radius = 10
        else:
            color = 'green'
            radius = 8

        popup_content = f"""
        <b>Magnitude {row['magnitude']}</b><br>
        Location: {row['place']}<br>
        Time: {row['time'].strftime('%Y-%m-%d %H:%M:%S')}<br>
        Depth: {row['depth']:.1f} km<br>
        <a href="{row['url']}" target="_blank">USGS Details</a>
        """

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            popup=popup_content,
            color=color,
            fill=True,
            fillOpacity=0.7
        ).add_to(m)

    if region_bbox:
        folium.Rectangle(
            bounds=[[region_bbox[1], region_bbox[0]], [region_bbox[3], region_bbox[2]]],
            color='blue',
            weight=2,
            fillOpacity=0.1
        ).add_to(m)

    return m

def create_comprehensive_charts(df, analysis):
    """Create comprehensive visualization charts"""
    if df.empty:
        return []

    charts = []

    # Magnitude over time with trend - with error handling
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df['time'], y=df['magnitude'],
        mode='markers',
        marker=dict(
            size=df['magnitude'] * 2,
            color=df['magnitude'],
            colorscale='Reds',
            showscale=True
        ),
        name='Earthquakes'
    ))

    # Only add trend line if we have enough data points (at least 2)
    if len(df) >= 2:
        try:
            z = np.polyfit(range(len(df)), df['magnitude'], 1)
            p = np.poly1d(z)
            fig1.add_trace(go.Scatter(
                x=df['time'], y=p(range(len(df))),
                mode='lines',
                name='Trend',
                line=dict(color='blue', dash='dash')
            ))
        except (np.linalg.LinAlgError, ValueError) as e:
            # If polynomial fitting fails, just show the scatter plot without trend
            print(f"Trend analysis unavailable: {str(e)}")

    fig1.update_layout(
        title='Earthquake Magnitude Over Time with Trend',
        xaxis_title='Time',
        yaxis_title='Magnitude',
        height=400
    )
    charts.append(fig1)

    # Magnitude distribution histogram - only if we have data
    if len(df) > 0:
        fig2 = px.histogram(
            df, x='magnitude', nbins=min(20, len(df)),  # Limit bins to data size
            title='Magnitude Distribution',
            labels={'magnitude': 'Magnitude', 'count': 'Frequency'}
        )
        fig2.update_layout(height=400)
        charts.append(fig2)

    # Depth vs Magnitude scatter - only if we have data
    if len(df) > 0:
        fig3 = px.scatter(
            df, x='depth', y='magnitude', color='magnitude',
            title='Depth vs Magnitude Relationship',
            labels={'depth': 'Depth (km)', 'magnitude': 'Magnitude'}
        )
        fig3.update_layout(height=400)
        charts.append(fig3)

    # Hourly distribution - only if we have the data
    if 'hourly_distribution' in analysis and len(analysis['hourly_distribution']) > 0:
        fig4 = px.bar(
            x=analysis['hourly_distribution'].index,
            y=analysis['hourly_distribution'].values,
            title='Earthquake Activity by Hour of Day',
            labels={'x': 'Hour', 'y': 'Count'}
        )
        fig4.update_layout(height=400)
        charts.append(fig4)

    # Risk level distribution - only if we have the data
    if 'risk_distribution' in analysis and len(analysis['risk_distribution']) > 0:
        fig5 = px.pie(
            values=analysis['risk_distribution'].values,
            names=analysis['risk_distribution'].index,
            title='Risk Level Distribution'
        )
        fig5.update_layout(height=400)
        charts.append(fig5)

    return charts
