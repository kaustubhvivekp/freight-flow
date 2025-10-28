# Freight Flow Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://freight-flow.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![GitHub](https://img.shields.io/github/license/kaustubhvivekp/freight-flow)](https://github.com/kaustubhvivekp/freight-flow/blob/main/LICENSE)

Interactive dashboard displaying marine shipping patterns and trade flows using Statistics Canada data.

## Live Demo
[Click here to view the live dashboard](https://freight-flow.streamlit.app)

## Features
- TEU Volume Decomposition Analysis
- Marine Trade Flows Visualization
- Time Series Analysis
- Destination Analysis
- Interactive Filters
- Key Statistics Display

## Local Development
1. Clone the repository
```bash
git clone https://github.com/kaustubhvivekp/freight-flow.git
cd freight-flow
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
streamlit run app.py
```

## Data Source
Statistics Canada - Table 23-10-0269-01

## Technologies Used
- Python
- Streamlit
- Plotly
- Pandas
- StatsModels