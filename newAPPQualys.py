import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table

# Load CSV data
data = pd.read_csv('completeee.csv')
dx = pd.read_csv('History.csv')

# Get unique categories from the 'IP' column
IPs = data['IP'].unique()

# Initialize Dash app
app = Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1('Qualys Scan Reports', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': IP, 'value': IP} for IP in IPs],
        value=IPs[0] if len(IPs) > 0 else None
    ),
    html.Br(),
    html.Div(id='data-table-container'),
    html.H4('Severity based on IP AVG'),
    dcc.Graph(id='severity-histogram'),
    html.H4('Severity and Titles by IP'),
    dcc.Graph(id='severity-scatter'),
    html.H4('Evolution of Vulnerabilities Detected'),
    dcc.Graph(id='vulnerabilities-evolution'),
    html.H4('Severity based on IP'),
    dcc.Graph(id='severity-line'),
])

# Define callback to update data table and graphs
@app.callback(
    Output('data-table-container', 'children'),
    Output('severity-histogram', 'figure'),
    Output('severity-scatter', 'figure'),
    Output('vulnerabilities-evolution', 'figure'),
    Output('severity-line', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_content(selected_ip):
    if selected_ip:
        filtered_data = data[data['IP'] == selected_ip]
        table = dash_table.DataTable(
            data=filtered_data.to_dict('records'),
            columns=[{"name": i, "id": i} for i in filtered_data.columns],
            page_size=10
        )

        # Update graphs
        hist_fig = px.histogram(filtered_data, x='IP', y='Severity', histfunc='avg')
        scatter_fig = px.scatter(filtered_data, x='IP', y='Title', color='Severity')
        line_fig = px.line(filtered_data, x='IP', y='Severity')
        evolution_fig = px.line(dx, x="Session", y=dx.columns)

        return table, hist_fig, scatter_fig, evolution_fig, line_fig
    else:
        return html.Div("No data available."), {}, {}, {}, {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
