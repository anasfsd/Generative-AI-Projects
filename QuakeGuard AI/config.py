# API Keys & Configurations

GROQ_API_KEY = "YOUR_GROQ_API_KEY"

MAGNITUDE_COLORS = {
    'Low': '#00ff00',
    'Moderate': '#ffff00',
    'High': '#ff8000',
    'Severe': '#ff0000',
    'Extreme': '#800000'
}

RISK_THRESHOLDS = {
    'low': {'count': 5, 'max_magnitude': 3.0},
    'moderate': {'count': 10, 'max_magnitude': 4.5},
    'high': {'count': 20, 'max_magnitude': 5.5},
    'severe': {'count': 30, 'max_magnitude': 6.5},
    'extreme': {'count': 50, 'max_magnitude': 7.0}
}

EMERGENCY_PROTOCOLS = {
    'low': "Monitor situation. No immediate action required.",
    'moderate': "Stay alert. Review emergency plans.",
    'high': "Prepare emergency kit. Stay informed.",
    'severe': "Follow evacuation orders if issued. Seek shelter.",
    'extreme': "IMMEDIATE EVACUATION. Follow emergency services."
}
