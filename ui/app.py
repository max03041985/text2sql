import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import urllib.parse
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
st.set_page_config(page_title="BFSI Marketing Analytics", layout="wide")

st.title(" Marketing Analytics")
st.markdown("Natural Language to SQL Engine for Campaign Cohort Generation")

if "sql_result" not in st.session_state:
    st.session_state.sql_result = None

with st.form("query_form"):
    nl_query = st.text_area(
        "Enter analytics question (e.g., 'Top 5 cities by jewelry spend for active credit card holders with high propensity')", 
        height=100
    )
    submitted = st.form_submit_button("Generate Insights")

if submitted and nl_query:
    with st.spinner("Analyzing schema and generating SQL..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/text-to-sql", 
                json={"query": nl_query}, 
                timeout=180  # Increased timeout for first query
            )
            response.raise_for_status()
            st.session_state.sql_result = response.json()
            
        except requests.exceptions.HTTPError as e:
            # This will show the EXACT error from the backend!
            st.error(f"API Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: {e}")
            
    with st.spinner("Analyzing schema and generating SQL..."):
        try:
            response = requests.post(f"{API_BASE_URL}/api/v1/text-to-sql", json={"query": nl_query}, timeout=300)
            response.raise_for_status()
            st.session_state.sql_result = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            st.session_state.sql_result = None

if st.session_state.sql_result:
    res = st.session_state.sql_result
    
    st.subheader("💡 Logic Explanation")
    st.info(res["explanation"])
    
    with st.expander("View Generated SQL"):
        st.code(res["sql"], language="sql")
    
    st.subheader("📊 Data Preview & KPIs")
    if res["preview"]:
        df = pd.DataFrame(res["preview"])
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # Intelligent KPI prioritization: look for business-meaningful columns
        priority_keywords = ['spend', 'txn', 'amount', 'redemption', 'score', 'atv', 'count']
        meaningful_numeric_cols = [
            col for col in numeric_cols 
            if any(kw in col.lower() for kw in priority_keywords)
        ] or numeric_cols  # Fallback to all numeric if no match
        
        if meaningful_numeric_cols:
            cols = st.columns(min(len(meaningful_numeric_cols), 4))
            for i, col in enumerate(meaningful_numeric_cols[:4]):
                # Sum for transactional columns, average/max for scores/flags
                if 'score' in col.lower() or 'flag' in col.lower() or 'valid' in col.lower():
                    val = df[col].max() if len(df) == 1 else df[col].mean()
                    metric_format = "{:.2f}" if isinstance(val, float) else "{:,}"
                else:
                    val = df[col].sum() if len(df) > 1 else df[col].iloc[0]
                    metric_format = "{:,.2f}" if isinstance(val, float) else "{:,}"
                
                cols[i].metric(
                    label=col.replace("_", " ").title(), 
                    value=metric_format.format(val)
                )
        
        # Dynamic Charting
        if len(df) > 1 and len(numeric_cols) > 0:
            chart_col = st.selectbox("Select metric for chart", meaningful_numeric_cols)
            label_options = [c for c in df.columns if c not in numeric_cols]
            label_col = st.selectbox("Select dimension for chart", label_options or [df.columns[0]])
            
            fig = px.bar(df, x=label_col, y=chart_col, title=f"{chart_col.replace('_', ' ').title()} by {label_col.replace('_', ' ').title()}")
            st.plotly_chart(fig, use_container_width=True)
            
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📥 Full Cohort Export (>500k rows)")
        st.markdown("Uses direct backend server-side cursor streaming to bypass browser/memory limits.")
        encoded_sql = urllib.parse.quote(res["sql"])
        download_url = f"{API_BASE_URL}/api/v1/stream-csv?sql_query={encoded_sql}"
        
        st.markdown(
            f'<a href="{download_url}" target="_blank" style="display: inline-block; padding: 10px 20px; background-color: #FF4B4B; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">⬇️ Download Full CSV (Streaming)</a>',
            unsafe_allow_html=True
        )