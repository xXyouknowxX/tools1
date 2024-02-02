import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table
from dash.exceptions import PreventUpdate

# Load your CSV data
data = pd.read_csv('completeee.csv')
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Ensure 'Date' is datetime format

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Vulnerability Management Dashboard', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='ip-dropdown',
        options=[{'label': IP, 'value': IP} for IP in data['IP'].unique()],
        placeholder="Select IP",
        style={'margin': '10px'}
    ),
    dcc.Dropdown(
        id='severity-dropdown',
        options=[{'label': severity, 'value': severity} for severity in sorted(data['Severity'].unique())],
        placeholder="Select Severity",
        style={'margin': '10px'}
    ),
    html.Div(id='summary-stats', style={'margin': '20px'}),
    dcc.Graph(id='severity-histogram', style={'margin': '20px'}),
    dcc.Graph(id='severity-scatter', style={'margin': '20px'}),
    dcc.Graph(id='vulnerabilities-evolution', style={'margin': '20px'}),
    dcc.Graph(id='severity-line', style={'margin': '20px'}),
    dash_table.DataTable(
        id='vulnerability-table',
        columns=[{"name": i, "id": i} for i in data.columns],
        page_size=10,
        style_table={'overflowY': 'auto', 'width': '100%', 'minWidth': '100%'},
        filter_action="native",
        sort_action="native",
    ),
], style={'fontFamily': 'Arial'})

# Callback to update dashboard
@app.callback(
    [Output('summary-stats', 'children'),
     Output('severity-histogram', 'figure'),
     Output('severity-scatter', 'figure'),
     Output('vulnerabilities-evolution', 'figure'),
     Output('severity-line', 'figure'),
     Output('vulnerability-table', 'data')],
    [Input('ip-dropdown', 'value'),
     Input('severity-dropdown', 'value')]
)
def update_dashboard(selected_ip, selected_severity):
    filtered_data = data.copy()
    if selected_ip:
        filtered_data = filtered_data[filtered_data['IP'] == selected_ip]
    if selected_severity:
        filtered_data = filtered_data[filtered_data['Severity'] == selected_severity]
    
    if filtered_data.empty:
        raise PreventUpdate

    # Summary Stats
    total_vulnerabilities = len(filtered_data)
    severity_counts = filtered_data['Severity'].value_counts().to_dict()
    summary_stats = html.Div([
        html.H4(f'Total Vulnerabilities: {total_vulnerabilities}'),
        html.Ul([html.Li(f"{severity}: {count}") for severity, count in severity_counts.items()])
    ])

    # Severity Histogram
    hist_fig = px.histogram(filtered_data, x='Severity', title="Vulnerabilities by Severity")

    # Severity Scatter Plot
    scatter_fig = px.scatter(filtered_data, x='Date', y='Severity', color='Severity', title="Severity Over Time")

    # Vulnerabilities Evolution
    evolution_fig = px.line(filtered_data, x='Date', y='Severity', title="Vulnerability Severity Evolution", color='IP')

    # Severity Line Chart
    line_fig = px.line(filtered_data, x='IP', y='Severity', title="IP Severity Distribution", color='IP')

    return summary_stats, hist_fig, scatter_fig, evolution_fig, line_fig, filtered_data.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
