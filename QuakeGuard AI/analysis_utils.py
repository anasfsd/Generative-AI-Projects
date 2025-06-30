import numpy as np
from datetime import datetime
from config import RISK_THRESHOLDS

def calculate_risk_level(magnitude):
    """Calculate risk level based on magnitude"""
    if magnitude >= 7.0:
        return 'Extreme'
    elif magnitude >= 6.0:
        return 'Severe'
    elif magnitude >= 5.0:
        return 'High'
    elif magnitude >= 4.0:
        return 'Moderate'
    else:
        return 'Low'

def categorize_magnitude(magnitude):
    """Categorize magnitude for analysis"""
    if magnitude >= 7.0:
        return 'Major (≥7.0)'
    elif magnitude >= 6.0:
        return 'Strong (6.0-6.9)'
    elif magnitude >= 5.0:
        return 'Moderate (5.0-5.9)'
    elif magnitude >= 4.0:
        return 'Light (4.0-4.9)'
    else:
        return 'Minor (<4.0)'

def categorize_depth(depth):
    """Categorize depth for analysis"""
    if depth < 70:
        return 'Shallow (<70km)'
    elif depth < 300:
        return 'Intermediate (70-300km)'
    else:
        return 'Deep (>300km)'

def calculate_time_ago(time):
    """Calculate time ago in human readable format"""
    now = datetime.utcnow()
    diff = now - time

    if diff.days > 0:
        return f"{diff.days} day(s) ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour(s) ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute(s) ago"
    else:
        return "Just now"

def analyze_seismic_patterns(df):
    """Analyze seismic patterns and trends"""
    if df.empty:
        return {}

    analysis = {}

    try:
        # Only calculate distributions if we have data
        if len(df) > 0:
            analysis['hourly_distribution'] = df['hour_of_day'].value_counts().sort_index()
            analysis['daily_distribution'] = df['day_of_week'].value_counts()

        # Magnitude statistics - only if we have magnitude data
        if 'magnitude' in df.columns and len(df) > 0:
            analysis['magnitude_stats'] = {
                'mean': df['magnitude'].mean(),
                'median': df['magnitude'].median(),
                'std': df['magnitude'].std(),
                'max': df['magnitude'].max(),
                'min': df['magnitude'].min()
            }

        # Depth statistics - only if we have depth data
        if 'depth' in df.columns and len(df) > 0:
            analysis['depth_stats'] = {
                'mean': df['depth'].mean(),
                'median': df['depth'].median(),
                'std': df['depth'].std()
            }

        # Risk distribution - only if we have risk level data
        if 'risk_level' in df.columns and len(df) > 0:
            analysis['risk_distribution'] = df['risk_level'].value_counts()

        # Geographic center - only if we have multiple data points
        if len(df) > 1 and 'latitude' in df.columns and 'longitude' in df.columns:
            analysis['geographic_center'] = {
                'lat': df['latitude'].mean(),
                'lon': df['longitude'].mean()
            }

    except Exception as e:
        print(f"Error in pattern analysis: {str(e)}")
        return {}

    return analysis

def calculate_overall_risk(df):
    """Calculate overall risk assessment"""
    if df.empty:
        return 'low', "No recent seismic activity"

    count = len(df)
    max_magnitude = df['magnitude'].max()

    risk_score = 0

    if count >= RISK_THRESHOLDS['extreme']['count']:
        risk_score += 40
    elif count >= RISK_THRESHOLDS['severe']['count']:
        risk_score += 30
    elif count >= RISK_THRESHOLDS['high']['count']:
        risk_score += 20
    elif count >= RISK_THRESHOLDS['moderate']['count']:
        risk_score += 10

    if max_magnitude >= RISK_THRESHOLDS['extreme']['max_magnitude']:
        risk_score += 40
    elif max_magnitude >= RISK_THRESHOLDS['severe']['max_magnitude']:
        risk_score += 30
    elif max_magnitude >= RISK_THRESHOLDS['high']['max_magnitude']:
        risk_score += 20
    elif max_magnitude >= RISK_THRESHOLDS['moderate']['max_magnitude']:
        risk_score += 10

    if risk_score >= 60:
        risk_level = 'extreme'
    elif risk_score >= 40:
        risk_level = 'severe'
    elif risk_score >= 25:
        risk_level = 'high'
    elif risk_score >= 10:
        risk_level = 'moderate'
    else:
        risk_level = 'low'

    return risk_level, f"Risk Score: {risk_score}/80"
