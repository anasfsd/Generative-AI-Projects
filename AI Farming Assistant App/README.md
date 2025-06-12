# AI Climate & Smart Farming Assistant

A Streamlit application that provides AI-powered insights for climate monitoring and smart farming practices.

## Features

- Real-time weather data and forecasts
- Air quality monitoring
- Smart farming data analysis
- AI-powered climate insights
- PDF report generation

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   AIRVISUAL_API_KEY=your_airvisual_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Environment Variables

The following environment variables need to be set in your `.env` file:

- `GROQ_API_KEY`: Your Groq API key for AI model access
- `AIRVISUAL_API_KEY`: Your AirVisual API key for air quality data

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them periodically
- Use environment variables for all sensitive information

## Deployment on Hugging Face

1. Create a new Space on Hugging Face
2. Set up your environment variables in the Space settings
3. Deploy your application using the Hugging Face CLI or web interface

## License

MIT License 
