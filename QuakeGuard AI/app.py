import streamlit as st
from datetime import datetime
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from config import EMERGENCY_PROTOCOLS, REGION_BBOXES
from api_utils import fetch_earthquakes, get_groq_summary
from analysis_utils import analyze_seismic_patterns, calculate_overall_risk
from visualization import create_advanced_map, create_comprehensive_charts

def main():
    st.set_page_config(
        page_title="🌍 Advanced Earthquake Warning System",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .risk-high { color: #ff4444; font-weight: bold; }
    .risk-moderate { color: #ffaa00; font-weight: bold; }
    .risk-low { color: #44aa44; font-weight: bold; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        color: #222 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">🌍 Advanced Earthquake Warning System</h1>', unsafe_allow_html=True)
    st.markdown("### Real-time seismic monitoring with AI-powered risk assessment and emergency protocols")

    st.sidebar.header("⚙️ Configuration")

    region = st.sidebar.text_input(
        "🌍 Region (optional)",
        placeholder="e.g., California, Pakistan, Japan"
    )

    col1, col2 = st.sidebar.columns(2)
    with col1:
        min_magnitude = st.slider("📏 Min Magnitude", 1.0, 7.0, 2.5, 0.1)
    with col2:
        hours = st.slider("⏰ Hours", 1, 168, 24)

    with st.sidebar.expander("🔧 Advanced Options"):
        show_detailed_analysis = st.checkbox("Detailed Analysis", value=True)
        show_ai_summary = st.checkbox("AI Summary", value=True)
        show_emergency_protocols = st.checkbox("Emergency Protocols", value=True)

    region_bbox = REGION_BBOXES.get(region.strip().title()) if region else None

    if st.button("🔄 Refresh Data", type="primary"):
        st.rerun()

    with st.spinner("🌐 Fetching earthquake data..."):
        df = fetch_earthquakes(min_magnitude, hours, region_bbox, show_detailed_analysis)

    if df.empty:
        st.warning("⚠️ No recent earthquakes found matching your criteria.")
        st.info("💡 Try reducing the minimum magnitude or increasing the time range.")

        # Show a simple message when no data is available
        st.markdown("""
        <div class="metric-card">
            <h3>🚨 Current Risk Level: <span class="risk-low">LOW</span></h3>
            <p><strong>Risk Score:</strong> 0/80</p>
            <p><strong>Emergency Protocol:</strong> Monitor situation. No immediate action required.</p>
        </div>
        """, unsafe_allow_html=True)

        # Show tabs with appropriate messages
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ Map", "📊 Analytics", "📋 Data", "🤖 AI Analysis", "🚨 Emergency"])

        with tab1:
            st.subheader("🌍 Interactive Earthquake Map")
            st.info("No earthquake data available for map visualization")

        with tab2:
            st.subheader("📊 Advanced Analytics")
            st.info("No earthquake data available for analysis")

        with tab3:
            st.subheader("📋 Earthquake Data")
            st.info("No earthquake data available")

        with tab4:
            st.subheader("🤖 AI-Powered Analysis")
            if show_ai_summary:
                st.info("No earthquake data available for AI analysis")
            else:
                st.info("Enable AI Summary in Advanced Options to see AI analysis.")

        with tab5:
            st.subheader("🚨 Emergency Information")
            if show_emergency_protocols:
                st.markdown("""
                ### 🚨 Emergency Response Protocols

                **Immediate Actions During Earthquake:**
                - Drop, Cover, and Hold On
                - Stay indoors if you're inside
                - Move to open area if you're outside
                - Stay away from windows, mirrors, and heavy objects

                **After Earthquake:**
                - Check for injuries and provide first aid
                - Check for gas leaks and electrical damage
                - Listen to emergency broadcasts
                - Be prepared for aftershocks

                **Emergency Contacts:**
                - Emergency Services: 911 (US) / 112 (EU) / 999 (UK)
                - USGS Earthquake Information: https://earthquake.usgs.gov
                - Local Emergency Management: Check your local government website
                """)

                st.markdown("""
                ### 📊 Current Emergency Status
                - **Risk Level**: LOW
                - **Recommended Action**: Monitor situation. No immediate action required.
                - **Monitoring Required**: No
                """)
            else:
                st.info("Enable Emergency Protocols in Advanced Options to see emergency information.")
    else:
        st.success(f"✅ Found {len(df)} earthquakes in the last {hours} hours")
        st.write(f"🕐 Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

        risk_level, risk_score = calculate_overall_risk(df)

        st.markdown(f"""
        <div class="metric-card">
            <h3>🚨 Current Risk Level: <span class="risk-{risk_level}">{risk_level.upper()}</span></h3>
            <p><strong>Risk Score:</strong> {risk_score}</p>
            <p><strong>Emergency Protocol:</strong> {EMERGENCY_PROTOCOLS[risk_level]}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Earthquakes", len(df))
        with col2:
            st.metric("Max Magnitude", f"{df['magnitude'].max():.1f}")
        with col3:
            st.metric("Avg Magnitude", f"{df['magnitude'].mean():.2f}")
        with col4:
            st.metric("Avg Depth", f"{df['depth'].mean():.1f} km")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ Map", "📊 Analytics", "📋 Data", "🤖 AI Analysis", "🚨 Emergency"])

        with tab1:
            st.subheader("🌍 Interactive Earthquake Map")
            if not df.empty:
                try:
                    map_obj = create_advanced_map(df, region_bbox)
                    if map_obj:
                        st_folium(map_obj, width=800, height=500)
                    else:
                        st.info("Unable to create map visualization")
                except Exception as e:
                    st.error(f"Error creating map: {str(e)}")
                    st.info("Try adjusting your search criteria")
            else:
                st.info("No earthquake data available for map visualization")

        with tab2:
            st.subheader("📊 Advanced Analytics")
            if not df.empty:
                try:
                    analysis = analyze_seismic_patterns(df)

                    charts = create_comprehensive_charts(df, analysis)
                    for i, chart in enumerate(charts):
                        st.plotly_chart(chart, use_container_width=True)

                    if analysis:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("📈 Magnitude Statistics")
                            if 'magnitude_stats' in analysis:
                                stats_df = pd.DataFrame([analysis['magnitude_stats']]).T
                                stats_df.columns = ['Value']
                                st.dataframe(stats_df)
                            else:
                                st.info("Insufficient data for magnitude statistics")

                        with col2:
                            st.subheader("📊 Risk Distribution")
                            if 'risk_distribution' in analysis and len(analysis['risk_distribution']) > 0:
                                risk_df = pd.DataFrame(analysis['risk_distribution'])
                                risk_df.columns = ['Count']
                                st.dataframe(risk_df)
                            else:
                                st.info("No risk distribution data available")
                except Exception as e:
                    st.error(f"Error in analytics: {str(e)}")
                    st.info("Try adjusting your search criteria or check your internet connection")
            else:
                st.info("No earthquake data available for analysis")

        with tab3:
            st.subheader("📋 Earthquake Data")
            if not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    magnitude_filter = st.multiselect(
                        "Filter by Magnitude Category",
                        options=df['magnitude_category'].unique(),
                        default=df['magnitude_category'].unique()
                    )
                with col2:
                    risk_filter = st.multiselect(
                        "Filter by Risk Level",
                        options=df['risk_level'].unique(),
                        default=df['risk_level'].unique()
                    )

                filtered_df = df[
                    (df['magnitude_category'].isin(magnitude_filter)) &
                    (df['risk_level'].isin(risk_filter))
                ]

                st.dataframe(
                    filtered_df[['time', 'place', 'magnitude', 'depth', 'risk_level', 'time_ago', 'url']],
                    use_container_width=True
                )

                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"earthquakes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

        with tab4:
            st.subheader("🤖 AI-Powered Analysis")
            if show_ai_summary and not df.empty:
                with st.spinner("🤖 Generating AI analysis..."):
                    analysis = analyze_seismic_patterns(df)
                    risk_level, risk_score = calculate_overall_risk(df)

                    prompt = f"""
                    As an expert seismologist and emergency response specialist, provide a comprehensive analysis of the following earthquake data:

                    SUMMARY STATISTICS:
                    - Total earthquakes: {len(df)}
                    - Time period: {hours} hours
                    - Magnitude range: {df['magnitude'].min():.1f} - {df['magnitude'].max():.1f}
                    - Average magnitude: {df['magnitude'].mean():.2f}
                    - Risk level: {risk_level.upper()}
                    - Risk score: {risk_score}

                    EARTHQUAKE DATA:
                    {df[['time', 'place', 'magnitude', 'depth']].head(20).to_string(index=False)}

                    Please provide:
                    1. **Risk Assessment**: Detailed evaluation of current seismic risk
                    2. **Pattern Analysis**: Identification of any concerning patterns or trends
                    3. **Regional Impact**: Specific implications for affected areas
                    4. **Safety Recommendations**: Detailed safety advice for the public
                    5. **Emergency Preparedness**: Specific actions people should take
                    6. **Monitoring Recommendations**: What to watch for in coming hours/days

                    Be thorough, specific, and actionable in your response.
                    """

                    summary = get_groq_summary(prompt)
                    st.markdown(summary)
            else:
                st.info("Enable AI Summary in Advanced Options to see AI analysis.")

        with tab5:
            st.subheader("🚨 Emergency Information")
            if show_emergency_protocols:
                st.markdown("""
                ### 🚨 Emergency Response Protocols

                **Immediate Actions During Earthquake:**
                - Drop, Cover, and Hold On
                - Stay indoors if you're inside
                - Move to open area if you're outside
                - Stay away from windows, mirrors, and heavy objects

                **After Earthquake:**
                - Check for injuries and provide first aid
                - Check for gas leaks and electrical damage
                - Listen to emergency broadcasts
                - Be prepared for aftershocks

                **Emergency Contacts:**
                - Emergency Services: 911 (US) / 112 (EU) / 999 (UK)
                - USGS Earthquake Information: https://earthquake.usgs.gov
                - Local Emergency Management: Check your local government website
                """)

                st.markdown(f"""
                ### 📊 Current Emergency Status
                - **Risk Level**: {risk_level.upper()}
                - **Recommended Action**: {EMERGENCY_PROTOCOLS[risk_level]}
                - **Monitoring Required**: {'Yes' if risk_level in ['high', 'severe', 'extreme'] else 'No'}
                """)
            else:
                st.info("Enable Emergency Protocols in Advanced Options to see emergency information.")

if __name__ == "__main__":
    main()
