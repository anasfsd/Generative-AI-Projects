import streamlit as st
from groq import Groq
import requests
import pandas as pd
from datetime import datetime, timedelta
import pycountry
from fpdf import FPDF
import io
import base64
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import plotly.express as px
import plotly.graph_objects as go
import unicodedata
from config import GROQ_API_KEY, AIRVISUAL_API_KEY, DEFAULT_MODEL
import os
from dotenv import load_dotenv

from utils.weather_utils import get_weather, get_historical_weather, get_air_quality
from utils.pdf_utils import generate_pdf
from utils.constants import SYSTEM_PROMPTS, EXAMPLE_QUERIES, CSS_STYLE

# Load environment variables
load_dotenv()

# Get API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AIRVISUAL_API_KEY = os.getenv("AIRVISUAL_API_KEY")
DEFAULT_MODEL = "llama3-70b-8192"

# === INIT Groq CLIENT ===
client = Groq(api_key=GROQ_API_KEY)

# === PAGE CONFIG ===
st.set_page_config(
    page_title="🌱 AI Climate & Smart Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CSS STYLING ===
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# === HEADER ===
st.markdown("<h1 class='title'>🌾 AI Climate & Smart Farming Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Real-time AI insights + live weather data</p>", unsafe_allow_html=True)
st.markdown("---")

# === SIDEBAR ===
st.sidebar.header("🌟 Features")
page = st.sidebar.radio(
    "Choose your tool:",
    [
        "AI Assistant Chat",
        "Weather Data",
        "Smart Farming CSV Analysis",
    ]
)

# === MULTI-TURN CHAT ===
if page == "AI Assistant Chat":
    st.subheader("🧠 AI Climate & Farming Chat Assistant")
    option = st.selectbox(
        "Choose a use case:",
        list(SYSTEM_PROMPTS.keys())
    )
    st.markdown(f"💡 *Example*: {EXAMPLE_QUERIES[option]}")

    user_input = st.text_area("Enter your question or describe your situation:")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("Send to AI") and user_input.strip():
        with st.spinner("Thinking..."):
            messages = [
                {"role": "system", "content": SYSTEM_PROMPTS[option]},
            ]
            # Append chat history for multi-turn
            for chat in st.session_state.chat_history:
                messages.append({"role": "user", "content": chat["user"]})
                messages.append({"role": "assistant", "content": chat["ai"]})
            # Add current user input
            messages.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
            )
            ai_response = response.choices[0].message.content

            # Save chat
            st.session_state.chat_history.append({"user": user_input, "ai": ai_response})

            # Clear input box
            st.rerun()

    if st.session_state.chat_history:
        st.markdown("### 🕘 Conversation History")
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"<div class='user-input'>You:</div><div>{chat['user']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='ai-response'>{chat['ai']}</div>", unsafe_allow_html=True)

        # Add PDF download button
        if st.button("Download Chat as PDF"):
            pdf_bytes = generate_pdf(st.session_state.chat_history)
            st.download_button(
                label="Click to Download PDF",
                data=pdf_bytes,
                file_name="climate_advice.pdf",
                mime="application/pdf"
            )

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# === WEATHER DATA PAGE ===
elif page == "Weather Data":
    st.subheader("🌍 Advanced Weather & Environmental Data")

    location_method = st.radio(
        "Choose location input method:",
        ["Enter City", "Select Country"]
    )

    location = None
    if location_method == "Enter City":
        location = st.text_input("Enter a city or location (e.g., Los Angeles, Delhi):")
    elif location_method == "Select Country":
        country = st.selectbox("Select a country:", [country.name for country in pycountry.countries])
        city = st.text_input("Enter city name:")
        location = f"{city}, {country}" if city else None

    if location:
        tab1, tab2, tab3 = st.tabs(["Current Weather", "Historical Data", "Air Quality"])

        with tab1:
            if st.button("Get Current Weather"):
                with st.spinner("Fetching data..."):
                    weather_data = get_weather(location)
                    if weather_data is None:
                        st.error("Failed to fetch weather data for this location.")
                    else:
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"### Current Weather in {weather_data['location']}:")
                            st.write(f"- Description: {weather_data['description']}")
                            st.write(f"- Temperature: {weather_data['temperature_C']} °C")
                            st.write(f"- Humidity: {weather_data['humidity_%']} %")
                            st.write(f"- Wind Speed: {weather_data['wind_speed_m/s']} m/s")

                        with col2:
                            fig = go.Figure()
                            fig.add_trace(go.Indicator(
                                mode="gauge+number",
                                value=weather_data['temperature_C'],
                                title={'text': "Temperature (°C)"},
                                gauge={'axis': {'range': [-20, 40]},
                                       'bar': {'color': "darkgreen"}}
                            ))
                            st.plotly_chart(fig)

        with tab2:
            days = st.slider("Select number of days for historical data:", 1, 30, 7)
            if st.button("Get Historical Weather"):
                with st.spinner("Fetching historical data..."):
                    hist_data = get_historical_weather(location, days)
                    if hist_data is None:
                        st.error("Failed to fetch historical weather data.")
                    else:
                        daily = hist_data['daily']
                        df = pd.DataFrame({
                            'Date': pd.date_range(start=daily['time'][0], periods=len(daily['time'])),
                            'Max Temp': daily['temperature_2m_max'],
                            'Min Temp': daily['temperature_2m_min'],
                            'Precipitation': daily['precipitation_sum'],
                            'Wind Speed': daily['wind_speed_10m_max']
                        })

                        # Create temperature range plot
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=df['Date'],
                            y=df['Max Temp'],
                            name='Max Temperature',
                            line=dict(color='red')
                        ))
                        fig.add_trace(go.Scatter(
                            x=df['Date'],
                            y=df['Min Temp'],
                            name='Min Temperature',
                            line=dict(color='blue'),
                            fill='tonexty'
                        ))
                        fig.update_layout(
                            title='Temperature Range Over Time',
                            xaxis_title='Date',
                            yaxis_title='Temperature (°C)',
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig)

                        # Create precipitation and wind speed plot
                        fig2 = go.Figure()
                        fig2.add_trace(go.Bar(
                            x=df['Date'],
                            y=df['Precipitation'],
                            name='Precipitation',
                            marker_color='lightblue'
                        ))
                        fig2.add_trace(go.Scatter(
                            x=df['Date'],
                            y=df['Wind Speed'],
                            name='Wind Speed',
                            line=dict(color='orange'),
                            yaxis='y2'
                        ))
                        fig2.update_layout(
                            title='Precipitation and Wind Speed',
                            xaxis_title='Date',
                            yaxis_title='Precipitation (mm)',
                            yaxis2=dict(
                                title='Wind Speed (m/s)',
                                overlaying='y',
                                side='right'
                            )
                        )
                        st.plotly_chart(fig2)

        with tab3:
            if st.button("Get Air Quality Data"):
                with st.spinner("Fetching air quality data..."):
                    aq_data = get_air_quality(location, AIRVISUAL_API_KEY)
                    if aq_data is None:
                        st.error("Failed to fetch air quality data.")
                    else:
                        st.markdown(f"### Air Quality in {location}")
                        current = aq_data['current']

                        # Create air quality gauges
                        col1, col2, col3 = st.columns(3)

                        # Define parameters
                        params = {
                            'pm10': {'name': 'PM10 (μg/m³)', 'range': [0, 100]},
                            'pm2_5': {'name': 'PM2.5 (μg/m³)', 'range': [0, 50]},
                            'ozone': {'name': 'Ozone (μg/m³)', 'range': [0, 100]},
                            'nitrogen_dioxide': {'name': 'Nitrogen Dioxide (μg/m³)', 'range': [0, 100]},
                            'sulphur_dioxide': {'name': 'Sulphur Dioxide (μg/m³)', 'range': [0, 100]}
                        }

                        # Display gauges for first 3 parameters
                        for i, param in enumerate(['pm2_5', 'pm10', 'ozone']):
                            if param in current and current[param] is not None:
                                with [col1, col2, col3][i]:
                                    fig = go.Figure(go.Indicator(
                                        mode="gauge+number",
                                        value=current[param],
                                        title={'text': params[param]['name']},
                                        gauge={'axis': {'range': params[param]['range']},
                                               'bar': {'color': "darkgreen"}}
                                    ))
                                    st.plotly_chart(fig)

                        # Display other pollutants
                        st.markdown("### Other Pollutants")
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'nitrogen_dioxide' in current and current['nitrogen_dioxide'] is not None:
                                st.write(f"- Nitrogen Dioxide: {current['nitrogen_dioxide']} μg/m³")
                        with col2:
                            if 'sulphur_dioxide' in current and current['sulphur_dioxide'] is not None:
                                st.write(f"- Sulphur Dioxide: {current['sulphur_dioxide']} μg/m³")

# === SMART FARMING CSV ANALYSIS PAGE ===
elif page == "Smart Farming CSV Analysis":
    st.subheader("🌱 AI-Powered Farming Data Analysis")
    uploaded_file = st.file_uploader("Upload your farming dataset (CSV)", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ Data loaded successfully!")

            # Create tabs for different analyses
            tab1, tab2 = st.tabs(["Data Explorer", "AI Insights"])

            with tab1:
                st.markdown("### Dataset Preview")
                st.dataframe(df.head(5))

                if st.checkbox("Show Summary Statistics"):
                    st.markdown("### Summary Statistics")
                    st.write(df.describe().transpose())

                # Interactive visualizations
                numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
                if numeric_cols:
                    col1, col2 = st.columns(2)
                    with col1:
                        x_axis = st.selectbox("X-Axis", numeric_cols)
                    with col2:
                        y_axis = st.selectbox("Y-Axis", numeric_cols)

                    if x_axis and y_axis:
                        fig = px.scatter(
                            df,
                            x=x_axis,
                            y=y_axis,
                            title=f"{y_axis} vs {x_axis}",
                            trendline="ols",
                            color_discrete_sequence=["#2E7D32"]
                        )
                        st.plotly_chart(fig)

                    # Correlation heatmap
                    if len(numeric_cols) > 1:
                        st.markdown("### Correlation Matrix")
                        corr = df[numeric_cols].corr()
                        fig = px.imshow(corr,
                                        text_auto=True,
                                        aspect="auto",
                                        color_continuous_scale="Greens")
                        st.plotly_chart(fig)

            with tab2:
                st.markdown("### AI-Powered Farming Insights")
                st.info("Ask specific questions about your farming data to get actionable insights")

                analysis_prompt = st.text_area(
                    "What insights would you like? (Examples below):",
                    "Analyze this farming data and provide key insights:",
                    height=100
                )

                st.caption("Examples: 'Suggest optimal crops for this region', 'Identify yield patterns', "
                           "'Recommend irrigation improvements', 'Predict harvest timing'")

                if st.button("Generate AI Insights", type="primary"):
                    with st.spinner("🧠 Analyzing with AI..."):
                        # Prepare data context
                        context = f"Dataset has {len(df)} rows and columns: {', '.join(df.columns)}\n"
                        context += f"First 3 rows:\n{df.head(3).to_string(index=False)}"

                        # Get AI analysis
                        messages = [
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert agricultural data scientist. Analyze farming datasets and provide: "
                                    "1. Actionable insights for improving crop yield "
                                    "2. Recommendations based on climate patterns "
                                    "3. Resource optimization strategies "
                                    "4. Sustainable farming practices "
                                    "Use bullet points and specific numbers when possible."
                                )
                            },
                            {
                                "role": "user",
                                "content": f"{analysis_prompt}\n\n{context}"
                            }
                        ]

                        response = client.chat.completions.create(
                            model=DEFAULT_MODEL,
                            messages=messages,
                            temperature=0.3
                        )
                        insights = response.choices[0].message.content
                        st.markdown(f"<div class='insight-box'>{insights}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error processing data: {str(e)}")
    else:
        st.info("👆 Upload a CSV file containing your farming data to get started")

# === FOOTER ===
st.markdown("---")
st.markdown(
    "<small>🔋 Powered by <b>llama3-70b-8192</b> on Groq • Real-time data from Open-Meteo API</small>",
    unsafe_allow_html=True
) 
