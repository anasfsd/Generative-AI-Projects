# System prompts for different use cases
SYSTEM_PROMPTS = {
    "Track Pollution": (
        "You are an expert environmental scientist. "
        "Help users understand pollution levels in air, water, or soil using scientific reasoning. "
        "Provide actionable recommendations for improvement."
    ),
    "Carbon Emissions": (
        "You are a sustainability advisor. "
        "Estimate and explain carbon emissions, suggest reductions and eco-friendly alternatives. "
        "Include cost-benefit analysis and ROI calculations."
    ),
    "Predict Climate Patterns": (
        "You are a climate researcher. Predict or explain regional climate changes using current and historical data. "
        "Include statistical analysis and confidence intervals."
    ),
    "Smart Farming Advice": (
        "You are an AI-powered farming assistant. Help users with crop selection, irrigation, pest control, and yield optimization. "
        "Focus on sustainable practices and resource efficiency."
    ),
}

# Example queries for each use case
EXAMPLE_QUERIES = {
    "Track Pollution": "e.g., What's the air quality near Lahore right now?",
    "Carbon Emissions": "e.g., How can a factory reduce CO2 output sustainably?",
    "Predict Climate Patterns": "e.g., What climate changes are expected in sub-Saharan Africa?",
    "Smart Farming Advice": "e.g., Best crops to grow in dry conditions in Uganda?",
}

# CSS styling for the application
CSS_STYLE = """
    <style>
    .main {
        background-color: #f9f9f9;
        color: #222;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .title {
        text-align: center;
        color: #2E7D32;
        font-weight: 800;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
        color: #4CAF50;
    }
    .history-box {
        background-color: #e8f5e9;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 8px;
        border-left: 5px solid #66bb6a;
        color: #000000;
    }
    .ai-response {
        background-color: #c8e6c9;
        padding: 10px;
        margin-bottom: 15px;
        border-radius: 10px;
        white-space: pre-wrap;
        color: #000000;
    }
    .user-input {
        background-color: #dcedc8;
        padding: 8px;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 5px;
        color: #000000;
    }
    .download-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 10px 0;
    }
    .insight-box {
        background-color: #e1f5fe;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #0288d1;
        color: #000000;
        font-weight: 500;
        line-height: 1.6;
    }
    </style>
""" 
