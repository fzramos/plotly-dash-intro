import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pandas.io.formats import style
import plotly.express as px
from dash.dependencies import Input, Output

# Get dataset and get sample
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = 'ISO-8859-1',
                            dtype={'Div1Airport': str,
                                    'Div1TailNum': str,
                                    'Div2Airport': str,
                                    'Div2TailNum': str})
df = airline_data.sample(n=2500, random_state=0)

# Creating Charts for overall dataset
# fig1 = px.pie(df, values='Flights', names='DistanceGroup', 
#              title='Distance group proportion by flights')
# fig2 = px.bar(df, x='Flights', y='DistanceGroup', orientation='h',
#              title='Flights per Distance group')


app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Flight Delay Time Statistics',
                                style={'textAlign':'right'}),
                                html.Div(children=["Input Year:", 
                                        dcc.Input(id='in-yr', value='2011'),
                                        ], style={'font-size': 30}
                                ),
                                html.Br(),
                                html.Br(),
                                html.Div([ # Goal here is 2 graphs on 1 row
                                    html.Div(dcc.Graph(id='chart-1')),
                                    html.Div(dcc.Graph(id='chart-2')),
                                ], style={'display': 'flex'}),
                                html.Div([ # Goal here is 2 graphs on 1 line
                                    html.Div(dcc.Graph(id='chart-3')),
                                    html.Div(dcc.Graph(id='chart-4')),
                                ], style={'display': 'flex'}),
                                html.Div(dcc.Graph(id='chart-5'), style={'width':'65%'})
                                ])

@app.callback(
    [
        Output(component_id='chart-1', component_property='figure'),
        Output(component_id='chart-2', component_property='figure'),
        Output(component_id='chart-3', component_property='figure'),
        Output(component_id='chart-4', component_property='figure'),
        Output(component_id='chart-5', component_property='figure'),
    ],
    Input(component_id='in-yr', component_property='value')
)
def create_charts_for_yr(yr):
    df_yr = df.loc[df['Year']==int(yr)]
    df_carrier_yr_delays = df_yr.groupby(['Reporting_Airline', 'Month'], as_index=False)\
        [['DepDelayMinutes','WeatherDelay','ArrDelay','NASDelay','SecurityDelay','LateAircraftDelay']]\
        .mean()
    # need to convert all non-minute columns from hours to minutes
    df_carrier_yr_delays[['WeatherDelay','ArrDelay','NASDelay','SecurityDelay','LateAircraftDelay']] = \
        df_carrier_yr_delays[['WeatherDelay','ArrDelay','NASDelay','SecurityDelay','LateAircraftDelay']] * 60
    fig1 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='DepDelayMinutes',
                        color='Reporting_Airline')
    fig2 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='WeatherDelay',
                        color='Reporting_Airline')
    fig3 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='NASDelay',
                        color='Reporting_Airline')
    fig4 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='SecurityDelay',
                        color='Reporting_Airline')  
    fig5 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='LateAircraftDelay',
                        color='Reporting_Airline')                        
    return [fig1, fig2, fig3, fig4, fig5]


if __name__ == "__main__":
    app.run_server()