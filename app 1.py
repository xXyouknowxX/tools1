from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import csv

# Specify your original and new file paths
original_csv_path = 'Scan_Results_exper5gm_20240205_scan_1707037252_62308.csv'
cleaned_csv_path = 'cleaned_completeee.csv'

# Initialize Dash app
app = Dash(__name__)
# Clean the CSV file

def clean_csv_v2(input_filename, output_filename, header_row_index=7):
    with open(input_filename, 'r', encoding='utf-8') as infile, \
            open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        
        # Read all lines from the input file
        lines = infile.readlines()
        
        # Process the header row to remove surrounding quotes and any unwanted characters
        header = lines[header_row_index].strip()
        if header.startswith('"') and header.endswith('"'):
            header = header[1:-1]  # Remove the first and last character if they are quotes
        header = header.replace('""', '"')  # Replace double quotes with single quotes if needed
        
        # Optionally, remove quotes from each header field
        header_fields = header.split(';')
        header_fields = [field.strip('"') for field in header_fields]
        
        # Join the header fields back together, now cleaned, using the desired delimiter (e.g., comma)
        cleaned_header = ','.join(header_fields)
        
        # Write the cleaned header to the output file
        outfile.write(cleaned_header + '\n')
        
        # Write the rest of the file, starting from the row after the header
        for line in lines[header_row_index + 1:]:
            # Replace semicolons with commas for each row if changing delimiter
            # Optionally, strip surrounding quotes from each field in the row
            cleaned_line = line.strip().replace('";"', '","').strip('"')
            outfile.write(cleaned_line + '\n')

            
# Load your CSV data
#data_types = {'IP': str, 'Severity': str, 'Title': str}
data = pd.read_csv('cleaned_completeee.csv',delimiter=',')
dx = pd.read_csv('History.csv')



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