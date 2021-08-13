# Creating a Dash dashboard that includes user input
# Goal 1: 
#   Create an interactive chart allowing users to get top 10 airlines 
#   by flight in a year
# Goal 2:
#   Create an interactive chart with user input to get top 10 airlines
#    by flight for a given destination state

import dash
import pandas as pd
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Get dataset and get sample
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = 'ISO-8859-1',
                            dtype={'Div1Airport': str,
                                    'Div1TailNum': str,
                                    'Div2Airport': str,
                                    'Div2TailNum': str})

# df = airline_data.sample(n=500, random_state=0)
df = airline_data

# Creating Charts for overall dataset
fig1 = px.pie(df, values='Flights', names='DistanceGroup', 
             title='Distance group proportion by flights')
fig2 = px.bar(df, x='Flights', y='DistanceGroup', orientation='h',
             title='Flights per Distance group')

# Initializing app
app=dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Interactive Dashboard', style={'textAlign':'center'}),
                                html.P('Interactive Dashboard about U.S. Airline Flights', style={'textAlign':'center'}),
                                html.Div([
                                    html.H2('Interactive Graph 1'),
                                    html.Div([
                                        'Year:', dcc.Input(id='input-yr-1', value='2018'),
                                    ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(dcc.Graph(id='bar-plot-1'))
                                ]),
                                html.Div([
                                    html.H2('Interactive Graph 2'),
                                    html.Div([
                                        'Year:', dcc.Input(id='input-yr-2', value='2018'),
                                    ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(dcc.Graph(id='line-plot-1'))
                                ]),
                                html.Div([
                                    html.H2('Interactive Graph 3 (Multi-Input)'),
                                    html.Div([
                                        'Year:', dcc.Input(id='input-yr-3', value='2018'),
                                        '\tDestination State Abbr.:', dcc.Input(id='input-symbol-1', value='AZ')
                                    ]),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(dcc.Graph(id='bar-plot-2'))
                                ]),
                                dcc.Graph(figure=fig1),
                                dcc.Graph(figure=fig2)
                                ])
# note: can't just add id to dcc components

@app.callback(Output(component_id='bar-plot-1', component_property='figure'),
                Input(component_id='input-yr-1', component_property='value'))
def graph_top10_yr(yr):
    df_yr = df[df['Year']==int(yr)]
    df_yr_top_airlines = df_yr.groupby('Reporting_Airline')['Flights'].sum().nlargest(10).reset_index()
    return px.bar(df_yr_top_airlines, y='Reporting_Airline', x='Flights', orientation='h')

@app.callback(Output(component_id='line-plot-1', component_property='figure'),
                Input(component_id='input-yr-2', component_property='value'))
def month_avg_delay_yr(yr):
    df_yr = df[df['Year']==int(yr)]
    df_avg_delay_month = df_yr.groupby('Month')['DepDelay'].mean().reset_index()
    return px.line(df_avg_delay_month, x='Month', y='DepDelay')

# Multiple Input Callback
@app.callback(Output(component_id='bar-plot-2', component_property='figure'),
                [
                    Input(component_id='input-yr-3', component_property='value'),
                    Input(component_id='input-symbol-1', component_property='value')
                ])
def graph_top10_yr_state(yr, state):
    df_yr = df.loc[(df['Year']==int(yr)) & (df['DestState']==state.upper())]
    df_yr_top_airlines = df_yr.groupby('Reporting_Airline')['Flights'].sum().nlargest(10).reset_index()
    return px.bar(df_yr_top_airlines, y='Reporting_Airline', x='Flights', orientation='h')

if __name__=='__main__':
    app.run_server(port=8054, host='localhost')

