# Freight Flow Analytics Dashboard

[![GitHub Pages](https://img.shields.io/badge/View-Dashboard-blue?style=for-the-badge&logo=github)](https://kaustubhvivekp.github.io/freight-flow/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

Interactive dashboard displaying marine shipping patterns and trade flows using Statistics Canada data.

## Live Dashboard
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