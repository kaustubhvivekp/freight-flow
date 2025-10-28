import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
import os
from pathlib import Path

# Create docs directory for GitHub Pages
docs_dir = Path('docs')
docs_dir.mkdir(exist_ok=True)

# Load data
df = pd.read_csv('shipping_focus_23100269.csv')
df['REF_DATE'] = pd.to_datetime(df['REF_DATE'])

# Generate TEU Volume Decomposition
teu_series = df[df['mode'] == 'TEU'].copy()
teu_series = teu_series.set_index('REF_DATE')['VALUE'].sort_index()
decomposition = seasonal_decompose(teu_series, period=12)

fig_teu = go.Figure()
fig_teu.add_trace(go.Scatter(x=teu_series.index, y=teu_series.values,
                        mode='lines+markers', name='Observed TEU'))
fig_teu.add_trace(go.Scatter(x=teu_series.index, y=decomposition.trend,
                        mode='lines', name='Trend', line=dict(dash='dot')))
fig_teu.update_layout(
    title='TEU Volume: Trend Analysis',
    height=600,
    template='plotly_white'
)
fig_teu.write_html(docs_dir / 'teu_analysis.html')

# Generate Marine Trade Flows Heatmap
marine_flows = df[df['mode'] == 'Marine'].copy()
monthly_flows = marine_flows.groupby(['REF_DATE', 'destination'])['VALUE'].sum().reset_index()
monthly_flows['Month'] = monthly_flows['REF_DATE'].dt.month

pivot_flows = monthly_flows.pivot_table(
    values='VALUE',
    index='Month',
    columns='destination',
    aggfunc='mean'
)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=pivot_flows.values,
    x=pivot_flows.columns,
    y=[f"{i:02d}" for i in pivot_flows.index],
    colorscale='RdYlBu'
))
fig_heatmap.update_layout(
    title='Marine Trade Flows: Average Monthly Pattern by Destination',
    height=600,
    template='plotly_white'
)
fig_heatmap.write_html(docs_dir / 'trade_flows.html')

# Generate main index page
index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Freight Flow Analytics Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; }
        .dashboard-item { margin-bottom: 30px; }
        .viz-container { height: 600px; border: 1px solid #ddd; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">🚢 Freight Flow Analytics Dashboard</h1>
        
        <div class="row dashboard-item">
            <div class="col-12">
                <h2>TEU Volume Analysis</h2>
                <div class="viz-container">
                    <iframe src="teu_analysis.html" width="100%" height="100%" frameborder="0"></iframe>
                </div>
            </div>
        </div>

        <div class="row dashboard-item">
            <div class="col-12">
                <h2>Marine Trade Flows</h2>
                <div class="viz-container">
                    <iframe src="trade_flows.html" width="100%" height="100%" frameborder="0"></iframe>
                </div>
            </div>
        </div>

        <footer class="mt-5 text-center">
            <p>Data source: Statistics Canada - Table 23-10-0269-01</p>
            <p>
                <a href="https://github.com/kaustubhvivekp/freight-flow" target="_blank" class="btn btn-outline-dark">
                    View on GitHub
                </a>
            </p>
        </footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

with open(docs_dir / 'index.html', 'w') as f:
    f.write(index_html)

print("Static dashboard files generated successfully in the docs directory!")