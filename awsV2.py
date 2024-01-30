import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

# Sample CSV data
data = pd.DataFrame({
    'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Value': [1, 2, 3, 4, 5, 6]
})

# Initialize Dash app
app = Dash(__name__)

# Define layout
app.layout = html.Div([
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'A', 'value': 'A'},
            {'label': 'B', 'value': 'B'},
            {'label': 'C', 'value': 'C'}
        ],
        value='A'
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
    filtered_data = data[data['Category'] == selected_category]
    table = html.Table([
        html.Tr([html.Th(col) for col in filtered_data.columns]),
        *[html.Tr([html.Td(filtered_data.iloc[i][col]) for col in filtered_data.columns]) for i in range(len(filtered_data))]
    ])
    return table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)