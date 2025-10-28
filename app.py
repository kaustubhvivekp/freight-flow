import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np

# Set page config
st.set_page_config(
    page_title="Freight Flow Analytics",
    page_icon="🚢",
    layout="wide"
)

# Title and description
st.title("🚢 Freight Flow Analytics")
st.markdown("""
This dashboard provides insights into marine shipping patterns and trade flows using Statistics Canada data.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('shipping_focus_23100269.csv')
    df['REF_DATE'] = pd.to_datetime(df['REF_DATE'])
    return df

# Load the data
try:
    df = load_data()
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
selected_mode = st.sidebar.selectbox(
    "Select Mode",
    options=sorted(df['mode'].unique())
)

# Main content
# Create two columns for the layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("TEU Volume Decomposition")
    # TEU decomposition plot
    if selected_mode == 'TEU':
        teu_series = df[df['mode'] == 'TEU'].copy()
        teu_series = teu_series.set_index('REF_DATE')['VALUE'].sort_index()
        
        decomposition = seasonal_decompose(teu_series, period=12)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=teu_series.index, y=teu_series.values,
                            mode='lines+markers', name='Observed TEU'))
        fig.add_trace(go.Scatter(x=teu_series.index, y=decomposition.trend,
                            mode='lines', name='Trend', line=dict(dash='dot')))
        fig.update_layout(title='TEU Volume: Trend Analysis',
                         height=400)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Marine Trade Flows")
    # Marine trade flows heatmap
    if selected_mode == 'Marine':
        marine_flows = df[df['mode'] == 'Marine'].copy()
        monthly_flows = marine_flows.groupby(['REF_DATE', 'destination'])['VALUE'].sum().reset_index()
        monthly_flows['Month'] = monthly_flows['REF_DATE'].dt.month
        
        pivot_flows = monthly_flows.pivot_table(
            values='VALUE',
            index='Month',
            columns='destination',
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_flows.values,
            x=pivot_flows.columns,
            y=[f"{i:02d}" for i in pivot_flows.index],
            colorscale='RdYlBu'
        ))
        fig.update_layout(title='Average Monthly Trade Flows by Destination',
                         height=400)
        st.plotly_chart(fig, use_container_width=True)

# Time series analysis
st.subheader("Time Series Analysis")
filtered_df = df[df['mode'] == selected_mode]

# Group by date
time_series = filtered_df.groupby('REF_DATE')['VALUE'].sum().reset_index()

# Create line plot
fig = px.line(time_series, x='REF_DATE', y='VALUE',
              title=f'{selected_mode} Values Over Time')
st.plotly_chart(fig, use_container_width=True)

# Value statistics
st.subheader("Key Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Value", f"{filtered_df['VALUE'].sum():,.0f}")
with col2:
    st.metric("Average Monthly Value", f"{filtered_df.groupby('REF_DATE')['VALUE'].sum().mean():,.0f}")
with col3:
    # Calculate year-over-year growth
    yearly = filtered_df.groupby(filtered_df['REF_DATE'].dt.year)['VALUE'].sum()
    if len(yearly) > 1:
        yoy_growth = ((yearly.iloc[-1] / yearly.iloc[-2]) - 1) * 100
        st.metric("Year-over-Year Growth", f"{yoy_growth:.1f}%")

# Destination analysis
if st.checkbox("Show Destination Analysis"):
    st.subheader("Destination Analysis")
    
    # Group by destination
    dest_analysis = filtered_df.groupby('destination')['VALUE'].agg(['sum', 'mean', 'std']).reset_index()
    dest_analysis.columns = ['Destination', 'Total Value', 'Average Value', 'Standard Deviation']
    
    # Sort by total value
    dest_analysis = dest_analysis.sort_values('Total Value', ascending=False)
    
    # Display as table
    st.dataframe(dest_analysis)
    
    # Create bar chart
    fig = px.bar(dest_analysis, x='Destination', y='Total Value',
                 title=f'Total {selected_mode} Value by Destination')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Data source: Statistics Canada - Table 23-10-0269-01")

# Social sharing section
st.markdown("---")
st.markdown("### Share this dashboard")
col1, col2, col3 = st.columns(3)
with col1:
    linkedin_url = "https://www.linkedin.com/sharing/share-offsite/?url=" + st.experimental_get_query_params().get("url", ["https://freight-flow.streamlit.app"])[0]
    st.markdown(f"[![Share on LinkedIn](https://img.shields.io/badge/Share_on-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]({linkedin_url})")
with col2:
    twitter_url = "https://twitter.com/intent/tweet?text=Check%20out%20this%20Freight%20Flow%20Analytics%20Dashboard!%20&url=" + st.experimental_get_query_params().get("url", ["https://freight-flow.streamlit.app"])[0]
    st.markdown(f"[![Share on Twitter](https://img.shields.io/badge/Share_on-Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)]({twitter_url})")
with col3:
    github_url = "https://github.com/kaustubhvivekp/freight-flow"
    st.markdown(f"[![View on GitHub](https://img.shields.io/badge/View_on-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)]({github_url})")