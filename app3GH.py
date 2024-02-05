from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Specify your original and new file paths
original_csv_path = 'completeee.csv'
cleaned_csv_path = 'cleaned_completeee.csv'

# Clean the CSV file
clean_csv(original_csv_path, cleaned_csv_path)

# Now, load the cleaned CSV into a Pandas DataFrame
data = pd.read_csv(cleaned_csv_path)

# Continue with your data processing...


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
    dcc.Graph(id='severity-3d-scatter', style={'margin': '20px'}),  # Placeholder for the 3D scatter plot
    dash_table.DataTable(
        id='vulnerability-table',
        columns=[{"name": i, "id": i} for i in data.columns],
        page_size=10,
        style_table={'overflowY': 'auto', 'width': '100%', 'minWidth': '100%'},
        filter_action="native",
        sort_action="native",
    ),
], style={'fontFamily': 'Arial'})

@app.callback(
    [Output('summary-stats', 'children'),
     Output('severity-histogram', 'figure'),
     Output('severity-scatter', 'figure'),
     Output('severity-3d-scatter', 'figure'),  # Add this output for the 3D scatter plot
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

    # Severity Histogram with distinct colors
    hist_fig = px.histogram(filtered_data, x='Severity', color='Severity',
                            title="Vulnerabilities by Severity",
                            category_orders={"Severity": ["Critical", "High", "Medium", "Low"]},
                            color_discrete_map=severity_to_color())

    # Before plotting, wrap the 'Title' text for readability
    filtered_data['WrappedTitle'] = filtered_data['Title'].apply(lambda x: wrap_text(x, width=15))

    # Then use 'WrappedTitle' for the y-axis labels in your scatter plot
    scatter_fig = px.scatter(filtered_data, x='Severity', y='WrappedTitle', color='Severity', title="Severity by Title")
    scatter_fig.update_layout(xaxis_tickangle=-45)  # Optionally rotate x-axis labels for better readability

    
    
    # Example 3D Scatter Plot
    # Use 'WrappedTitle' for hover text in your 3D scatter plot for better readability
    scatter_3d_fig = px.scatter_3d(filtered_data, x='IP', y='Severity', z='Risk Score' if 'Risk Score' in filtered_data.columns else 'Title',
                               color='Severity', title="3D View: IP, Severity, and Title",
                               hover_name='WrappedTitle')

    return summary_stats, hist_fig, scatter_fig, scatter_3d_fig, filtered_data.to_dict('records')

def wrap_text(text, width=10):
    """Wrap text with a given width."""
    if len(text) <= width:
        return text
    return '<br>'.join(text[i:i+width] for i in range(0, len(text), width))


def severity_to_color():
    """Function to provide a color map for severity levels."""
    return {
        'Critical': 'red',
        'High': 'orange',
        'Medium': 'yellow',
        'Low': 'green',
        'Unknown': 'grey'  # Handle any severity levels not explicitly listed
    }


def clean_csv(input_filename, output_filename, header_row_index=7):
    """
    Reads an input CSV file, skips rows until the header row, and writes the rest to an output CSV file.
    
    :param input_filename: Path to the input CSV file.
    :param output_filename: Path to the cleaned output CSV file.
    :param header_row_index: The 0-based index of the row containing the header (default is 7 for row 8).
    """
    with open(input_filename, 'r', newline='', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Skip rows until the header row
        for _ in range(header_row_index):
            next(reader)
        
        # Write the rest of the rows
        for row in reader:
            writer.writerow(row)


if __name__ == '__main__':
    app.run_server(debug=True)
