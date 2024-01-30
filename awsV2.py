import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

# Load CSV data
data = pd.read_csv('your_data.csv')

# Get unique categories from the 'Category' column
categories = data['Category'].unique()

# Initialize Dash app
app = Dash(__name__)

# Define layout
app.layout = html.Div([
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': category, 'value': category} for category in categories],
        value=categories[0] if categories else None  # Set default value to the first category
    ),
    html.Br(),
    html.Div(id='data-table-container')
])

# Define callback to update data table
@app.callback(
    Output('data-table-container', 'children'),
    [Input('category-dropdown', 'value')]
)
def update_data_table(selected_category):
    if selected_category:
        filtered_data = data[data['Category'] == selected_category]
        table = html.Table([
            html.Tr([html.Th(col) for col in filtered_data.columns]),
            *[html.Tr([html.Td(filtered_data.iloc[i][col]) for col in filtered_data.columns]) for i in range(len(filtered_data))]
        ])
        return table
    else:
        return html.Div("No data available for the selected category.")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)