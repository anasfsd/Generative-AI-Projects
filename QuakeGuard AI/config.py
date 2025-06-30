# Configuration and Constants
GROQ_API_KEY = ""

# Color schemes for different magnitude levels
MAGNITUDE_COLORS = {
    'Low': '#00ff00',      # Green
    'Moderate': '#ffff00', # Yellow
    'High': '#ff8000',     # Orange
    'Severe': '#ff0000',   # Red
    'Extreme': '#800000'   # Dark Red
}

# Risk assessment thresholds
RISK_THRESHOLDS = {
    'low': {'count': 5, 'max_magnitude': 3.0},
    'moderate': {'count': 10, 'max_magnitude': 4.5},
    'high': {'count': 20, 'max_magnitude': 5.5},
    'severe': {'count': 30, 'max_magnitude': 6.5},
    'extreme': {'count': 50, 'max_magnitude': 7.0}
}

# Emergency protocols
EMERGENCY_PROTOCOLS = {
    'low': "Monitor situation. No immediate action required.",
    'moderate': "Stay alert. Review emergency plans.",
    'high': "Prepare emergency kit. Stay informed.",
    'severe': "Follow evacuation orders if issued. Seek shelter.",
    'extreme': "IMMEDIATE EVACUATION. Follow emergency services."
}

# Region bounding boxes
REGION_BBOXES = {
    "California": [-125, 32, -114, 42],
    "Pakistan": [60, 23, 77, 37],
    "Japan": [129, 31, 146, 45],
    "Chile": [-75, -56, -66, -17],
    "Turkey": [25, 36, 45, 43],
    "Indonesia": [95, -11, 141, 6],
    "India": [68, 6, 97, 37],
    "Mexico": [-118, 14, -86, 33],
    "USA": [-125, 24, -66, 49],
    "World": [-180, -90, 180, 90]
}
