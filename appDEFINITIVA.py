from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import csv
import glob  # Import glob module

# Directory where your CSV files are stored
directory_path = 'path/to/your/csv/files/'
csv_pattern = directory_path + '*.csv'  # Pattern to match all CSV files

# Function to clean a single CSV file (as before)
def clean_csv(input_filename, output_filename, header_row_index=7):
    with open(input_filename, 'r', newline='', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter=';', quotechar='"', escapechar='|')
        writer = csv.writer(outfile, delimiter=',', quotechar=' ', escapechar='|')
        
        for _ in range(header_row_index):
            next(reader)
        headers = next(reader)
        headers = [header.strip('"') for header in headers] and [header.replace('"', '') for header in headers]
        
        writer.writerow(headers)
        
        for row in reader:
            writer.writerow(row)

# Assuming column names are consistent across all CSV files
column_names = ['IP', 'DNS', 'NetBIOS', 'OS', 'IP Status', 'QID', 'Title', 'Type', 'Severity', 'Port', 'Protocol', 'FQDN', 'SSL', 'CVE ID', 'Vendor Reference', 'Bugtraq ID', 'Threat', 'Impact', 'Solution', 'Exploitability', 'Associated Malware', 'Results', 'PCI Vuln', 'Instance', 'Category']

# List to hold dataframes from each file
dataframes = []

# Process each file found by glob
for file_path in glob.glob(csv_pattern):
    # Generate a cleaned CSV path or use the same file if cleaning is not needed
    cleaned_csv_path = file_path.replace('.csv', '_cleaned.csv')
    clean_csv(file_path, cleaned_csv_path, header_row_index=7)  # Clean the file if needed
    
    # Load the cleaned CSV into a DataFrame
    df = pd.read_csv(cleaned_csv_path, delimiter=',', names=column_names, header=0, skiprows=7)
    dataframes.append(df)

# Concatenate all DataFrames into one
data = pd.concat(dataframes, ignore_index=True)
dx = pd.read_csv('History.csv')  # Assuming this is another file you need

# Initialize Dash app
app = Dash(__name__)


# App layout
app.layout = html.Div([
    html.H1('Vulnerability Management Dashboard', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='ip-dropdown',
        options=[{'label': IP, 'value': IP} for IP in data['IP'].unique()],
        value= None,
        placeholder="Select IP",
        style={'margin': '10px'}
    ),
    dcc.Dropdown(
        id='severity-dropdown',
        options=[{'label': '5', 'value': '5'},
                 {'label': '4', 'value': '4'},
                 {'label': '3', 'value': '3'},
                 {'label': '2', 'value': '2'},
                 {'label': '1', 'value': '1'}
                ],
        placeholder="Select Severity",
        style={'margin': '10px'}
    ),
    html.H4('Evolution of Vulnerabilities Detected'),
    dcc.Graph(id='vulnerabilities-evolution'),
    html.Div(id='summary-stats', style={'margin': '20px'}),
    dcc.Graph(id='severity-histogram', style={'margin': '20px'}),
    dcc.Graph(id='severity-scatter', style={'overflow': 'scroll','height':'800px'}),
    dcc.Graph(id='severity-3d-scatter', style={'margin': '20px','height':'800px'}),  # Placeholder for the 3D scatter plot
    dash_table.DataTable(
        id='vulnerability-table',
        columns=[{"name": i, "id": i} for i in data.columns],
        page_size=50,
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
     Output('vulnerability-table', 'data'),
     Output('vulnerabilities-evolution', 'figure'),],
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
        raise Exception
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

    # Severity Scatter Plot
    scatter_fig = px.scatter(filtered_data, x='Severity', y='Title', color='Severity', title="Severity by Title")
    
    # Example 3D Scatter Plot
    scatter_3d_fig = px.scatter_3d(filtered_data, x='IP', y='Title', z='Severity',
                                   color='Severity', title="3D View: IP, Severity, and Title")

    evolution_fig = px.line(dx, x="Session", y=dx.columns)

    return summary_stats, hist_fig, scatter_fig, scatter_3d_fig, filtered_data.to_dict('records'), evolution_fig

def severity_to_color():
    """Function to provide a color map for severity levels."""
    return {
        'Critical': 'red',
        'High': 'orange',
        'Medium': 'yellow',
        'Low': 'green',
        'Unknown': 'grey'  # Handle any severity levels not explicitly listed
    }

if __name__ == '__main__':
    app.run_server(debug=True)