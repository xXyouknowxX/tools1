import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # Import required for using go.Figure
from dash import Dash, dcc, html, Input, Output, dash_table
from dash.exceptions import PreventUpdate

# Load your CSV data
data = pd.read_csv('completeee.csv')

# Assuming your CSV doesn't actually have a 'Date' column, so we'll skip this part
# If you have other columns like 'Risk Score', ensure they're formatted correctly

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
    dcc.Graph(id='vulnerabilities-evolution', style={'margin': '20px'}),  # Placeholder for future implementation
    dcc.Graph(id='severity-line', style={'margin': '20px'}),  # Placeholder for future implementation
    dash_table.DataTable(
        id='vulnerability-table',
        columns=[{"name": i, "id": i} for i in data.columns],
        page_size=10,
        style_table={'overflowY': 'auto', 'width': '100%', 'minWidth': '100%'},
        filter_action="native",
        sort_action="native",
    ),
], style={'fontFamily': 'Arial'})

# Additional function to map severity to colors
def severity_to_color(severity):
    color_map = {
        'Critical': 'red',
        'High': 'orange',
        'Medium': 'yellow',
        'Low': 'green',
    }
    return color_map.get(severity, 'blue')  # Default to 'blue' if severity level is unknown

@app.callback(
    [Output('summary-stats', 'children'),
     Output('severity-histogram', 'figure'),
     Output('severity-scatter', 'figure'),
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
        return html.Div("No data available for the selected filters."), {}, {}, []

    # Summary Stats
    total_vulnerabilities = len(filtered_data)
    severity_counts = filtered_data['Severity'].value_counts().to_dict()
    summary_stats = html.Div([
        html.H4(f'Total Vulnerabilities: {total_vulnerabilities}'),
        html.Ul([html.Li(f"{severity}: {count}") for severity, count in severity_counts.items()])
    ])

    # Severity Histogram with distinct colors
    hist_fig = go.Figure()
    for severity in sorted(data['Severity'].unique()):
        filtered = filtered_data[filtered_data['Severity'] == severity]
        hist_fig.add_trace(go.Histogram(x=filtered['Severity'], name=severity,
                                        marker_color=severity_to_color(severity)))

    hist_fig.update_layout(title="Vulnerabilities by Severity", barmode='stack')
    
    # Severity Scatter Plot (Adjusted for Titles)
    scatter_fig = px.scatter(filtered_data, x='Severity', y='Title', color='Severity', title="Severity by Title")

    # Returning the updated figures and data table
    return summary_stats, hist_fig, scatter_fig, filtered_data.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
