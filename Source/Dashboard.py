import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go



# Read the cleaned data from the csv file
crime_df = pd.read_csv('Data/crime_data_cleaned.csv')

# Convert the datetime_occ column to datetime
crime_df['datetime_occ'] = pd.to_datetime(crime_df['datetime_occ'])

num_crimes = len(crime_df)
years = crime_df['datetime_occ'].dt.year.unique()

# Create the Dash app
app = dash.Dash(__name__)

# Title of the app
title = 'LOS ANGELES CRIMES FROM 2020 TO PRESENT'

# Section 1: Overview about number of crimes and crime distribution by area


app.layout = html.Div([
    html.H1(title, style={'text-align': 'center'}),
    html.H2('Overview'),


    
    html.H4('Crime Distribution in each Year'),
    dcc.Dropdown(
        options=[{'label': str(year), 'value': year} for year in years],
        clearable=False,
        multi=True,
        id='year-dropdown',  
        placeholder="Select years",
        value=years[-3:],
        style={'width': "50%", 'padding': '5px', 'float':'left'},
    ),

    html.Div([
                # html.H4('Total Number of Crimes'),
                html.H3(num_crimes, style={'font-size': '40px', 'font-weight':"bold", 'text-align': 'center'}),
                
            ], 
            style={'width': "30%", 
                   'float':'left',
        }
    ),

    dcc.Graph(id='num-crimes-line-plot', figure={}, 
                style={'width': "60%", 'float':'left', 'height':'700px'}, ),
    
   

    # Pie chart for crime part distribution
    dcc.Graph(
        figure=px.pie(crime_df['part_1_2'].value_counts(), values=crime_df['part_1_2'].value_counts().values, names=crime_df['part_1_2'].value_counts().index, labels={'part_1_2': 'Crime Part'}),
    style={'width': "35%", 'margin': '10px', 'float':'left', 'height':'350px'}),

    # Graph for status description distribution
    dcc.Graph(
        figure=px.bar(crime_df['status_desc'].value_counts(), y=crime_df['status_desc'].value_counts().index, x=crime_df['status_desc'].value_counts().values, labels={'x': 'Number of Crimes', 'y': 'Status'}, orientation='h'),
    style={'width': "35%", 'margin': '10px', 'float':'left', 'height':'300px'}),
        

 
    dcc.Graph(
        figure=px.bar(crime_df['area_name'].value_counts(), x=crime_df['area_name'].value_counts().index, y=crime_df['area_name'].value_counts().values, labels={'y': 'Number of Crimes'}),
    style={'width': "100%", 'margin': '10px', 'float':'left', 'height':'600px'}),

    # Draw top 10 crime types barh plot
    dcc.Graph(id='crime-types-bar-plot',
                figure=px.bar(crime_df['crm_cd_desc'].value_counts()[:10], y=crime_df['crm_cd_desc'].value_counts()[:10].index, x=crime_df['crm_cd_desc'].value_counts()[:10].values, labels={'x': 'Number of Crimes'}),
                    style={'width': "60%", 'float':'left', 'height':'300px'}, ),
    # Draw top 10 weapon used barh plot
    dcc.Graph(id='weapon-bar-plot',
                figure=px.bar(crime_df['weapon_desc'].value_counts()[:10], y=crime_df['weapon_desc'].value_counts()[:10].index, x=crime_df['weapon_desc'].value_counts()[:10].values, labels={'x': 'Number of Crimes'}),
                    style={'width': "40%", 'float':'left', 'height':'300px'}, ),
    # Draw top 10 premis_desc barh plot
    dcc.Graph(id='premis-bar-plot',
                figure=px.bar(crime_df['premis_desc'].value_counts()[:10], y=crime_df['premis_desc'].value_counts()[:10].index, x=crime_df['premis_desc'].value_counts()[:10].values, labels={'x': 'Number of Crimes'}),
                    style={'width': "40%", 'float':'left', 'height':'500px'}, ),

    # Crime location dot map
    dcc.Graph(id='crime-location-dot-map',
                figure={}, 
                style={'width': "60%", 'float':'left', 'height':'500px'},),

    # Draw top victim age histogram
    dcc.Graph(id='victim-age-hist',
                figure=px.histogram(crime_df, x='vict_age', nbins=30, labels={'x': 'Victim Age'}),
                    style={'width': "50%", 'float':'left', 'height':'500px'},  ),
    # Draw all victim descent bar plot
    dcc.Graph(id='victim-descent-bar-plot',
                figure={}, 
                style={'width': "50%", 'float':'left', 'height':'500px'},),

],style={'padding': '10px',},)

@app.callback(
    Output('num-crimes-line-plot', 'figure'),
    Input('year-dropdown', 'value')
)
def update_num_crimes_line_plot(years_selected):
    
    dff = crime_df[crime_df['datetime_occ'].dt.year.isin(years_selected)]
    dff['month_occ'] = dff['datetime_occ'].dt.month

    fig = px.line()

    for year in years_selected:
        year_df = dff[dff['datetime_occ'].dt.year == year]
        year_df = year_df.groupby('month_occ').size().reset_index(name='num_crimes')
        fig.add_scatter(x=year_df['month_occ'], y=year_df['num_crimes'], mode='lines+markers', name=year)

    fig.update_layout(
        title='Number of Crimes in each Month', 
        xaxis_title='Month', 
        yaxis_title='Number of Crimes',
        xaxis=dict(
            tickmode='array',
            tickvals=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            ticktext=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        )
    )
    return fig

@app.callback(
    Output('victim-descent-bar-plot', 'figure'),
    Input('year-dropdown', 'value')
)
def update_victim_descent_bar_plot(years_selected):
        # Group the data by victim descent and get the number of crimes for each victim sex
    victim_by_descent = crime_df[['vict_descent', 'vict_sex']].groupby(['vict_descent', 'vict_sex']).size().reset_index(name='count').sort_values(by='count', ascending=True)

    victim_by_descent['descent_desc'] = victim_by_descent['vict_descent'].map({'A': 'Other Asian', 'B': 'Black', 'C': 'Chinese', 'D': 'Cambodian', 'F': 'Filipino', 'G': 'Guamanian', 'H': 'Hispanic/Latin/Mexican', 'I': 'American Indian/Alaskan Native', 'J': 'Japanese', 'K': 'Korean', 'L': 'Laotian', 'O': 'Other', 'P': 'Pacific Islander', 'S': 'Samoan', 'U': 'Hawaiian', 'V': 'Vietnamese', 'W': 'White', 'Z': 'Asian Indian'})
    # Create the bar plot
    vict_descents_plot = px.bar(victim_by_descent, y='descent_desc', x='count', color='vict_sex',
             labels={'count': 'Count', 'descent_desc': 'Victim Descent'},orientation='h', title='Number of Crimes by Victim Descent')
    
    return vict_descents_plot

@app.callback(
    Output('crime-location-dot-map', 'figure'),
    Input('year-dropdown', 'value')
)
def update_crime_location_dot_map(years_selected):

    dff = crime_df[crime_df['datetime_occ'].dt.year == 2021]
    
    # Set up the Mapbox token (replace 'your_mapbox_token' with your actual Mapbox token)
    mapbox_token = 'pk.eyJ1IjoicGh1b25nbmFtMjU0IiwiYSI6ImNscW5hdHg4ZDNhY2Yya25wOTB4NW11cGMifQ.rqIAm8QhVlEmcgtwCwKG5A'

    # Set up the layout using Mapbox
    layout = go.Layout(
        mapbox=dict(
            accesstoken=mapbox_token,
            center=dict(
                lat=34.0522,  # Los Angeles latitude
                lon=-118.2437  # Los Angeles longitude
            ),
            zoom=10  # Set the initial zoom level
        )
    )

    trace = go.Scattermapbox(
        lat=dff['lat'],
        lon=dff['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
    )


    fig = go.Figure(data=[trace], layout=layout)

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)




