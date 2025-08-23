# analysis.py — risk, categorization, and pattern analysis
if 'magnitude' in df.columns:
analysis['magnitude_stats'] = {
'mean': df['magnitude'].mean(),
'median': df['magnitude'].median(),
'std': df['magnitude'].std(),
'max': df['magnitude'].max(),
'min': df['magnitude'].min()
}
if 'depth' in df.columns:
analysis['depth_stats'] = {
'mean': df['depth'].mean(),
'median': df['depth'].median(),
'std': df['depth'].std()
}
if 'risk_level' in df.columns:
analysis['risk_distribution'] = df['risk_level'].value_counts()
if len(df) > 1 and 'latitude' in df.columns and 'longitude' in df.columns:
analysis['geographic_center'] = {
'lat': df['latitude'].mean(),
'lon': df['longitude'].mean()
}
except Exception:
return {}
return analysis




def calculate_overall_risk(df: pd.DataFrame):
if df.empty:
return 'low', "Risk Score: 0/80"
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
