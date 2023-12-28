

"""
This script creates a dashboard using the Dash framework to visualize and analyze Los Angeles crime data from 2020 to the present. 
The dashboard includes multiple sections such as the number of crimes by years, crime details, and victim details. 
It uses various graphs and charts to present the data in an interactive and informative way.
"""

# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os 
import sys



# Read the cleaned data from the csv file
crime_df = pd.read_csv('../Data/crime_data_cleaned.csv')

# Convert the datetime_occ column to datetime
crime_df['datetime_occ'] = pd.to_datetime(crime_df['datetime_occ'])
# Get the unique years in the data
years = crime_df['datetime_occ'].dt.year.unique()
# Title of the app
title = 'LOS ANGELES CRIMES FROM 2020 TO PRESENT'

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Add the title to the dashboard
    html.H1(title, style={'text-align': 'center', 'font-family': 'Arial', 'size': '120px'}),

    # ---------------------------------------------------------------------------------------------------
    # Section 1: Number of Crimes by Years
    html.Hr(),
    html.H2('NUMBER OF CRIMES BY YEARS', style={'text-align': 'center', 'font-family': 'Arial', 'size': '60px', 'color': 'grey'}),

    # Dropdown for selecting years
    dcc.Dropdown(
        options=[{'label': str(year), 'value': year} for year in years],
        clearable=False,
        multi=True,
        id='year-dropdown',
        placeholder="Select years",
        value=years,
        style={'width': "70%", 'padding': '5px', 'float': 'left', 'margin': '10px'},
    ),

    # Div for displaying the total number of crimes
    html.Div(
        [
            html.Div(
                id='num-crimes-div',
                style={'width': "70%", 'float': 'left', 'padding': '10px'}
            ),
        ],
        style={'border': '1px solid #ccc', 
               'border-radius': '5px', 
               'padding': '10px', 
               'margin-bottom': '10px', 
               'float': 'left', 
               'width': '11%', 
               'height': '130px',
               'background-color': '#f2f2f2'}
    ),

    # Graph for displaying the number of crimes in each year as a pie chart
    dcc.Graph(id='num-crimes-pie-chart', style={'width': "30%", 'float': 'left', 'height': '600px'}),

    # Graph for displaying the number of crimes in each area as a bar plot
    dcc.Graph(id='area-bar-plot', figure={}, style={'width': "60%", 'float': 'left', 'height': '600px'}),

    # Graph for displaying the number of crimes in each year as a line plot
    dcc.Graph(id='num-crimes-line-plot', figure={}, style={'width': "60%", 'float': 'left', 'height': '900px'}),

    # Graph for displaying the distribution of status descriptions
    dcc.Graph(id='status-desc-pie-chart', figure={}, style={'width': "35%", 'margin': '10px', 'float': 'left', 'height': '500px'}),

    # Graph for displaying the distribution of crime parts
    dcc.Graph(id='crime-part-pie-chart', figure={}, style={'width': "35%", 'margin': '10px', 'float': 'left', 'height': '400px'}),

    # ---------------------------------------------------------------------------------------------------
    # Section 2: Crime Details
    html.Hr(style={'margin-top': '50px', 'width': '100%', 'float': 'left'}),
    html.H2('CRIME DETAILS', style={'text-align': 'center', 'font-family': 'Arial', 'width': '100%', 'size': '60px', 'color': 'grey', 'float': 'left'}),

    # Graph for displaying the top 20 crime types with the highest number of crimes as a horizontal bar plot
    dcc.Graph(id='crime-types-bar-plot', figure={}, style={'width': "50%", 'float': 'left', 'height': '600px'}, clickData={'points': [{'label': 'VEHICLE - STOLEN', 'pointNumber': 19}]}),

    # Graph for displaying the crime locations as a dot map
    dcc.Graph(id='crime-location-dot-map', figure={}, style={'width': "50%", 'float': 'right', 'height': '1200px'}),

    # Graph for displaying the top 5 weapons used as a horizontal bar plot
    dcc.Graph(id='weapon-bar-plot', figure={}, style={'width': "50%", 'float': 'left', 'height': '300px'}),

    # Graph for displaying the top 5 premise descriptions as a horizontal bar plot
    dcc.Graph(id='premis-bar-plot', figure={}, style={'width': "50%", 'float': 'left', 'height': '300px'}),

    # ---------------------------------------------------------------------------------------------------
    # Section 3: Victim Details
    html.Hr(style={'margin-top': '50px', 'width': '100%', 'float': 'left'}),
    html.H2('VICTIM DETAILS', style={'text-align': 'center', 'font-family': 'Arial', 'width': '100%', 'size': '60px', 'color': 'grey', 'float': 'left'}),

    # Graph for displaying the histogram of victim ages
    dcc.Graph(id='victim-age-hist', figure={}, style={'width': "50%", 'float': 'left', 'height': '500px'}),

    # Graph for displaying the distribution of victim descents
    dcc.Graph(id='victim-descent-bar-plot', figure={}, style={'width': "50%", 'float': 'left', 'height': '500px'}),
], style={'font-family': 'Arial', 'background-color': '#f2f2f2'})

# ---------------------------------------------------------------------------------------------------
# Callbacks for updating the graphs based on user input

# Update the total number of crimes based on the selected years in the dropdown
@app.callback(
    Output('num-crimes-div', 'children'),
    [Input('year-dropdown', 'value')]
)
def update_num_crimes(years_selected):
    filtered_df = crime_df[crime_df['datetime_occ'].dt.year.isin(years_selected)]
    num_crimes = len(filtered_df)
    return [
        html.P('Total number of crimes', style={'font-size': '14px', 'text-align': 'left'}),
        html.H3(num_crimes, style={'font-size': '40px', 'font-weight': "bold",
                                    'text-align': 'left', 'margin': '0px', 'color': 'grey'})
    ]

# Update the pie chart for the number of crimes based on the selected years in the dropdown
@app.callback(
    Output('num-crimes-pie-chart', 'figure'),
    Input('year-dropdown', 'value')
)
def update_num_crimes_charts(years_selected):
    # Filter the data based on the selected years
    filtered_df = crime_df[crime_df['datetime_occ'].dt.year.isin(years_selected)]
    # Create the pie chart
    fig = px.pie(filtered_df, 
                 values=filtered_df['datetime_occ'].dt.year.value_counts().values, 
                 names=filtered_df['datetime_occ'].dt.year.value_counts().index
    )
    # Configure the pie chart
    fig.update_layout(title='Number of Crimes in each Year',  title_x=0.5, title_font_size=20, title_font_family='Arial')
    return fig

# Update the bar plot for the number of crimes in each area based on the selected years in the dropdown
@app.callback(
    Output('area-bar-plot', 'figure'),
    Input('year-dropdown', 'value')
)
def update_area_bar_plot(years_selected):
    # Filter the data based on the selected years
    filtered_df = crime_df[crime_df['datetime_occ'].dt.year.isin(years_selected)]
    filtered_df['year'] = filtered_df['datetime_occ'].dt.year
    # Group the data by year and area name and get the number of crimes for each area
    filtered_df = filtered_df.groupby(['year', 'area_name']).size().reset_index(name='count').sort_values(by='count', ascending=False)

    fig = go.Figure()
    # Add the bar plot for each year
    for year in years_selected:
        year_df = filtered_df[filtered_df['year'] == year]
        fig.add_trace(go.Bar(
            x=year_df['area_name'], y=year_df['count'], name=year, legendgroup='group'))

    fig.update_layout(
        barmode='stack',
        title='Number of Crimes in each Area',
        yaxis=dict(
            range=[0, 60000],
            tickmode='array',
            tickvals=['0', '10000', '20000',
                      '30000', '40000', '50000', '60000']
        ),
        legend=dict(
            tracegroupgap=10
        ),
        title_x=0.5,
        title_font_size=20,
        title_font_family='Arial'
    )

    return fig

# Update the line plot for the number of crimes in each month based on the selected years in the dropdown
@app.callback(
    Output('num-crimes-line-plot', 'figure'),
    Input('year-dropdown', 'value')
)
def update_num_crimes_line_plot(years_selected):

    # Filter the data based on the selected years
    filtered_df = crime_df[crime_df['datetime_occ'].dt.year.isin(years_selected)]
    filtered_df['month_occ'] = filtered_df['datetime_occ'].dt.month

    fig = px.line()

    # Add the line plot for each year
    for year in years_selected:
        year_df = filtered_df[filtered_df['datetime_occ'].dt.year == year]
        year_df = year_df.groupby('month_occ').size().reset_index(name='num_crimes')
        fig.add_scatter(x=year_df['month_occ'], y=year_df['num_crimes'], mode='lines+markers', name=year)

    fig.update_layout(
        title='Number of Crimes in each Month',
        xaxis_title='Month',
        yaxis_title='Number of Crimes',
        xaxis=dict(
            tickmode='array',
            tickvals=['1', '2', '3', '4', '5', '6',
                      '7', '8', '9', '10', '11', '12'],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis=dict(
            range=[0, 25000],
            tickmode='array',
            tickvals=['5000', '7500', '10000',
                      '12500', '15000', '17500', '20000', '22500', '25000']
        ),
        title_x=0.5,
        title_font_size=20,
        title_font_family='Arial'
    )
    return fig

# Update the pie chart for the distribution of status descriptions based on the selected years in the dropdown
@app.callback(
    Output('status-desc-pie-chart', 'figure'),
    Input('year-dropdown', 'value')
)
def update_status_desc_pie_chart(years_selected):
    # Filter the data based on the selected years
    filtered_df = crime_df[crime_df['datetime_occ'].dt.year.isin(years_selected)]
    # Create the pie chart
    fig = px.pie(filtered_df, 
                 values=filtered_df['status_desc'].value_counts().values, 
                 names=filtered_df['status_desc'].value_counts().index)
    # Configure the pie chart
    fig.update_layout(title='Status Description Distribution',  title_x=0.5, title_font_size=20, title_font_family='Arial')
    return fig

# Update the pie chart for the distribution of crime parts based on the selected years in the dropdown
@app.callback(
    Output('crime-part-pie-chart', 'figure'),
    Input('year-dropdown', 'value')
)
def update_crime_part_pie_chart(years_selected):
    # Filter the data based on the selected years
    filtered_df = crime_df[crime_df['datetime_occ'].dt.year.isin(years_selected)]
    # Group the data by crime part and get the number of crimes for each crime part
    filtered_df = filtered_df.groupby('part_1_2').size().reset_index(name='count')
    # Map the crime part to the actual crime part name
    filtered_df['part_1_2'] = filtered_df['part_1_2'].map({1: 'Serious Crimes', 2: 'Less Serious Crimes'})
    fig = px.pie(
        filtered_df, 
        values=filtered_df['count'], 
        names=filtered_df['part_1_2'], 
    )
    # Configure the pie chart
    fig.update_layout(title='Crime Part Distribution',  title_x=0.5, title_font_size=20, title_font_family='Arial')

    return fig

# Update the column colors of the crime-types-bar-plot based on the selected column
@app.callback(
    Output('crime-types-bar-plot', 'figure'),
    Input('crime-types-bar-plot', 'clickData')
)
def update_crime_types_bar_plot(clickData):
    selected_point = clickData['points'][0]['pointNumber']

    # Count the number of crimes for each crime type
    filtered_df = crime_df['crm_cd_desc'].value_counts().sort_values(ascending=True).tail(20)
    # Create the bar plot
    crime_fig = px.bar(filtered_df, 
                       y=filtered_df.index, 
                       x=filtered_df.values, 
                       orientation='h',
                )
    crime_fig.update_traces(selectedpoints=[selected_point],
                            unselected={'marker': {
                                'color': 'rgba(204,204,204,1)'}},
                            selected={'marker': {'color': 'rgba(0,116,217,1)'}}
                            )
    crime_fig.update_layout(
        xaxis_title='Number of Crimes', 
        yaxis_title=None, 
        title='Top 20 Crime Types (Click on a column to see details about that crime type)', 
        title_x=0.5, title_font_size=20, title_font_family='Arial'
    )

    return crime_fig

# Update the bar plot for the top 5 weapons used based on the selected crime type in the crime-types-bar-plot
@app.callback(
    Output('weapon-bar-plot', 'figure'),
    Input('crime-types-bar-plot', 'clickData')
)
def update_weapon_bar_plot(clickData):
    crime_type = clickData['points'][0]['label']

    # Filter your data based on the selected crime_type
    filtered_df = crime_df[crime_df['crm_cd_desc'] == crime_type]
    # Group the data by weapon description and get the number of crimes for each weapon
    filtered_df = filtered_df.groupby('weapon_desc').size().reset_index(name='count').sort_values(by='count', ascending=True).tail(5)

    weapon_fig = px.bar(filtered_df, 
                        y='weapon_desc', 
                        x='count', 
                        labels={'count': 'Number of Crimes'}, 
                    )
    weapon_fig.update_layout(xaxis_title='Number of Crimes',
                             yaxis_title=None,
                             title=f'Top 5 Weapons Used for {crime_type}',
                             title_x=0.5, title_font_size=20, title_font_family='Arial')
    return weapon_fig

# Update the bar plot for the top 5 premise descriptions based on the selected crime type in the crime-types-bar-plot
@app.callback(
    Output('premis-bar-plot', 'figure'),
    Input('crime-types-bar-plot', 'clickData')
)
def update_premis_bar_plot(clickData):
    crime_type = clickData['points'][0]['label']

    # Filter your data based on the selected crime_type
    filtered_df = crime_df[crime_df['crm_cd_desc'] == crime_type]
    # Group the data by premise description and get the number of crimes for each premise
    filtered_df = filtered_df.groupby('premis_desc').size().reset_index(name='count').sort_values(by='count', ascending=True).tail(5)

    premis_fig = px.bar(filtered_df, 
                        y='premis_desc', 
                        x='count', 
                        labels={'count': 'Number of Crimes'})
    premis_fig.update_layout(xaxis_title='Number of Crimes',
                                yaxis_title=None,
                                title=f'Top 5 Premise Descriptions for {crime_type}',
                                title_x=0.5, title_font_size=20, title_font_family='Arial')

    return premis_fig

# Update the dot map for the crime locations based on the selected crime type in the crime-types-bar-plot
@app.callback(
    Output('crime-location-dot-map', 'figure'),
    Input('crime-types-bar-plot', 'clickData')
)
def update_crime_location_dot_map(clickData):
    crime_type = clickData['points'][0]['label']
    # Filter your data based on the selected crime_type
    filtered_df = crime_df[crime_df['crm_cd_desc'] == crime_type]

    # Mapbox token gets from https://account.mapbox.com/access-tokens/
    mapbox_token = 'pk.eyJ1IjoicGh1b25nbmFtMjU0IiwiYSI6ImNscW5hdHg4ZDNhY2Yya25wOTB4NW11cGMifQ.rqIAm8QhVlEmcgtwCwKG5A'

    # Set up the layout using Mapbox
    layout = go.Layout(
        title=f'Crime Location Dot Map for {crime_type}',  # Add title
        mapbox=dict(
            accesstoken=mapbox_token,
            center=dict(
                lat=34.0589,  # Los Angeles latitude
                lon=-118.4648  # Los Angeles longitude
            ),
            zoom=9  # Set the initial zoom level
        ),
    )

    trace = go.Scattermapbox(
        lat=filtered_df['lat'],
        lon=filtered_df['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
    )

    fig = go.Figure(data=[trace], layout=layout)
    
    fig.update_layout(
        title_x=0.5, 
        title_font_size=20, 
        title_font_family='Arial'
    )

    return fig

# Not update, just use to define the plot outside the main layout
@app.callback(
    Output('victim-descent-bar-plot', 'figure'),
    Input('year-dropdown', 'value') # Input is not used
)
def update_victim_descent_bar_plot(years_selected):
    # Group the data by victim descent and get the number of crimes for each victim sex
    victim_by_descent = crime_df[['vict_descent', 'vict_sex']].groupby(['vict_descent', 'vict_sex']).size().reset_index(name='count').sort_values(by='count', ascending=True)
    # Map the victim descent to the actual victim descent name
    victim_by_descent['descent_desc'] = victim_by_descent['vict_descent'].map({'A': 'Other Asian', 'B': 'Black', 'C': 'Chinese', 'D': 'Cambodian', 'F': 'Filipino', 'G': 'Guamanian', 'H': 'Hispanic/Latin/Mexican',
                                                                              'I': 'American Indian/Alaskan Native', 'J': 'Japanese', 'K': 'Korean', 'L': 'Laotian', 'O': 'Other', 'P': 'Pacific Islander', 'S': 'Samoan', 'U': 'Hawaiian', 'V': 'Vietnamese', 'W': 'White', 'Z': 'Asian Indian'})
    # Create the bar plot
    vict_descents_plot = px.bar(victim_by_descent, 
                                y='descent_desc', 
                                x='count', 
                                color='vict_sex',
                                labels={'count': 'Count', 'descent_desc': 'Victim Descent'}, 
                                orientation='h', 
                            )
    vict_descents_plot.update_layout(xaxis_title='Count',
                                yaxis_title=None,
                                title='Victim Descent Distribution',
                                title_x=0.5, title_font_size=20, title_font_family='Arial')
    return vict_descents_plot


# Not update, just use to define the plot outside the main layout
@app.callback(
    Output('victim-age-hist', 'figure'),
    Input('crime-types-bar-plot', 'clickData') # Input is not used
)
def update_victim_age_hist(clickData):
    # Create the histogram
    fig = px.histogram(crime_df, 
                       x='vict_age', 
                       nbins=30, 
                       labels={'x': 'Victim Age'}, 
                    )
    fig.update_traces(marker_line_width=1, marker_line_color="white")
    fig.update_layout(xaxis_title='Victim Age',
                      yaxis_title='Count',
                      title='Victim Age Distribution',
                      title_x=0.5, title_font_size=20, title_font_family='Arial')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
