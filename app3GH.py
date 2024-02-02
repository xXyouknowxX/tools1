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
     Output('severity-3d-scatter', 'figure'),
     Output('severity-histogram', 'figure'),
     Output('severity-scatter', 'figure'),
     Output('vulnerabilities-evolution', 'figure'),
     Output('severity-line', 'figure'),
     Output('vulnerability-table', 'data')],
    [Input('ip-dropdown', 'value'),
     Input('severity-dropdown', 'value')]
)

# Additional function to map severity to colors
def severity_to_color(severity):
    color_map = {
        'Critical': 'red',
        'High': 'orange',
        'Medium': 'yellow',
        'Low': 'green',
    }
    return color_map.get(severity, 'blue')  # Default to 'blue' if severity level is unknown



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
    hist_fig = go.Figure()
    for severity in sorted(data['Severity'].unique()):
        filtered = filtered_data[filtered_data['Severity'] == severity]
        hist_fig.add_trace(go.Histogram(x=filtered['Severity'], name=severity,
                                        marker_color=severity_to_color(severity)))

    hist_fig.update_layout(title="Vulnerabilities by Severity", barmode='stack')
    
    # Severity Scatter Plot (Adjusted for Titles)
    scatter_fig = px.scatter(filtered_data, x='Severity', y='Title', color='Severity', title="Severity by Title")

    # Example 3D Scatter Plot
    # Assuming you have a 'Risk Score' column for this example. Adjust according to your data.
    if 'Risk Score' in filtered_data.columns:
        scatter_3d_fig = px.scatter_3d(filtered_data, x='IP', y='Severity', z='Risk Score',
                                        color='Severity', title="3D View: IP, Severity, and Risk Score")
    else:
        scatter_3d_fig = {"layout": {"title": "3D View: Data not available (Risk Score missing)"}}

    # Return updated figures
    return summary_stats, hist_fig, scatter_fig, evolution_fig, line_fig, scatter_3d_fig
if __name__ == '__main__':
    app.run_server(debug=True)
