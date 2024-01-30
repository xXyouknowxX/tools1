import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime

# Read the CSV file
df = pd.read_csv('qualys_scan_report.csv')

# Extract relevant columns
hosts = df['Host'].unique()
vulnerabilities_per_host = df.groupby('Host')['Vulnerability'].count()

# Truncate long host names
max_length = 10  # Define maximum length for truncated names
truncated_hosts = [host[:max_length] + '...' if len(host) > max_length else host for host in hosts]

# Generate artificial months for the average criticality score
# Assuming the data spans over multiple months
start_date = df['Date'].min()
end_date = df['Date'].max()
all_months = pd.date_range(start=start_date, end=end_date, freq='MS').strftime("%B %Y").tolist()

# Calculate average criticality score per host for each month
average_criticality_score_by_month = df.groupby(['Host', pd.Grouper(key='Date', freq='MS')])['Criticality'].mean().unstack(fill_value=0)

# Create Plotly dashboard
fig = make_subplots(rows=1, cols=2, subplot_titles=("Number of Vulnerabilities per Host", "Average Criticality Score per Host"))

# Add bar chart for number of vulnerabilities per host
fig.add_trace(go.Bar(x=truncated_hosts, y=vulnerabilities_per_host, name='Vulnerabilities'), row=1, col=1)

# Add line chart for average criticality score per host over months
for host in hosts:
    fig.add_trace(go.Scatter(x=all_months, y=average_criticality_score_by_month.loc[host], mode='lines', name=host), row=1, col=2)

# Update layout
fig.update_layout(title_text="Qualys Scan Report Dashboard")

# Show dashboard
fig.show()