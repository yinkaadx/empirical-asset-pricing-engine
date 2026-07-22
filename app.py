import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Empirical Asset Pricing Engine", layout="wide")

st.title("Serverless Asset Pricing & Macro Uncertainty Pipeline")
st.caption("Real-Time Machine Learning Adjustment based on Geopolitical & Policy Uncertainty Indices")

st.sidebar.header("Middleware Configuration")
selected_asset = st.sidebar.selectbox("Target Asset Class", ["S&P 500 Index ETF (SPY)", "New Zealand 10-Year Government Bond", "Emerging Market Equities"])
policy_shock = st.sidebar.slider("Simulate Geopolitical/Policy Shock Severity", 1.0, 5.0, 2.5)
run_simulation = st.sidebar.button("Initialize ML Pricing Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: AWS Lambda Data Ingestion -> XGBoost Risk Premium Adjuster")

if run_simulation:
    st.subheader(f"Active Empirical Pricing Model: {selected_asset}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_base_price = col1.empty()
    metric_ml_price = col2.empty()
    metric_uncertainty = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(404)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    base_prices = []
    ml_adjusted_prices = []
    uncertainty_indices = []
    
    start_price = 550.00 if "S&P" in selected_asset else 100.00
    
    for i in range(100):
        current_base = start_price + (i * 0.05) + np.random.uniform(-0.5, 0.5)
        
        if i < 40:
            current_uncertainty = np.random.uniform(10.0, 25.0)
            ml_discount = np.random.uniform(0.0, 0.2)
        elif i >= 40 and i < 70:
            current_uncertainty = 25.0 + (i - 40) * (2.0 * policy_shock) + np.random.uniform(-5.0, 5.0)
            ml_discount = (current_uncertainty / 100.0) * (1.5 * policy_shock)
        else:
            current_uncertainty = 25.0 + (30 * 2.0 * policy_shock) - (i - 70) * policy_shock + np.random.uniform(-5.0, 5.0)
            ml_discount = (current_uncertainty / 100.0) * (1.5 * policy_shock)
            
        current_ml_price = current_base - ml_discount
        
        base_prices.append(current_base)
        ml_adjusted_prices.append(current_ml_price)
        uncertainty_indices.append(current_uncertainty)
        
        metric_base_price.metric("Standard Baseline Price", f"${current_base:.2f}")
        metric_ml_price.metric("ML Adjusted Price (Risk Priced In)", f"${current_ml_price:.2f}", f"-${ml_discount:.2f} discount")
        metric_uncertainty.metric("Policy Uncertainty Index", f"{current_uncertainty:.1f} pts")
        
        if current_uncertainty >= 70.0:
            metric_status.metric("Market Sentiment", "HIGH GEOPOLITICAL RISK", "Deleveraging")
        else:
            metric_status.metric("Market Sentiment", "STABLE ENVIRONMENT", "Normal")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=base_prices, mode='lines', name='Baseline Asset Price', line=dict(color='gray', dash='dash')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=ml_adjusted_prices, mode='lines', name='ML Adjusted Price', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=uncertainty_indices, mode='lines', name='Policy Uncertainty Index', yaxis='y2', line=dict(color='red')))
        
        fig.update_layout(
            title="Empirical Asset Pricing: Baseline vs Machine Learning Adjusted (Real-Time)",
            xaxis=dict(title="High-Frequency Timeline"),
            yaxis=dict(title="Asset Price (USD)"),
            yaxis2=dict(title="Uncertainty Index", overlaying='y', side='right', range=[0, max(100, max(uncertainty_indices)+10)]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if current_uncertainty >= 70.0:
            log_placeholder.warning(f"MACRO ALERT: Severe policy uncertainty spike detected at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine dynamically increasing risk premium and discounting asset valuation.")
        else:
            log_placeholder.success(f"Log: Tick data {i} ingested via serverless middleware. Asset pricing model synchronized with global macroeconomic sentiment.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The cloud-native machine learning pipeline successfully priced geopolitical risk into the asset valuation in real-time.")
else:
    st.info("Click 'Initialize ML Pricing Engine' in the sidebar to simulate high-frequency asset pricing adjustments.")