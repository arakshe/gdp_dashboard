import dash
from plotly import graph_objs as go
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load CSV data
data = pd.read_csv('2014_world_gdp_with_codes.csv')

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("World GDP Dashboard"),

    # Choropleth map
    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth(
            data,
            locations="CODE",
            color="GDP (BILLIONS)",
            hover_name="COUNTRY",
            color_continuous_scale=px.colors.sequential.Plasma,
            title="World GDP Choropleth Map",
        )
    ),

    # Dropdown for selecting country
    dcc.Dropdown(
        id='country-dropdown',
        options=[
            {'label': country, 'value': country} for country in data['COUNTRY']
        ],
        value=data['COUNTRY'].iloc[0],  # Set the default value to the first country
    ),

    # Bar chart
    dcc.Graph(id='bar-chart'),

    # Slider for selecting GDP range with labels
    dcc.RangeSlider(
        id='gdp-slider',
        min=data['GDP (BILLIONS)'].min(),
        max=data['GDP (BILLIONS)'].max(),
        step=10,
        marks={
            data['GDP (BILLIONS)'].min(): 'Least GDP',
            data['GDP (BILLIONS)'].max(): 'Highest GDP'
        },
        value=[data['GDP (BILLIONS)'].min(), data['GDP (BILLIONS)'].max()],
    )
])

@app.callback(
    Output('choropleth-map', 'figure'),
    Output('bar-chart', 'figure'),
    Input('country-dropdown', 'value'),
    Input('gdp-slider', 'value')
)
def update_dashboard(selected_country, gdp_range):
    filtered_data = data[(data['GDP (BILLIONS)'] >= gdp_range[0]) & (data['GDP (BILLIONS)'] <= gdp_range[1])]

    # Create a figure for the choropleth map
    choropleth_map = px.choropleth(
        filtered_data,
        locations="CODE",
        color=filtered_data['GDP (BILLIONS)'],
        hover_name="COUNTRY",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="World GDP Choropleth Map"
    )

    # Create a figure for the bar chart
    bar_chart = px.bar(
        filtered_data,
        x="COUNTRY",
        y="GDP (BILLIONS)",
        title="GDP by Country",
        labels={"GDP (BILLIONS)": "GDP", "COUNTRY": "Country"},
        color=filtered_data['COUNTRY'] == selected_country  # Highlight the selected country in red
    ).update_yaxes(range=[0, 2000])

    return choropleth_map, bar_chart

if __name__ == '__main__':
    app.run_server(debug=True)
