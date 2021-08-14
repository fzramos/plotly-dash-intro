import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pandas.io.formats import style
import plotly.express as px
from dash.dependencies import Input, Output

# Get dataset and get sample
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = 'ISO-8859-1',
                            dtype={'Div1Airport': str,
                                    'Div1TailNum': str,
                                    'Div2Airport': str,
                                    'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Flight Delay Time Statistics',
                                style={
                                    'textAlign':'center',
                                    'font-size': 30,
                                    'color': '#503D36'
                                }),
                                html.Div(children=["Input Year:", 
                                        dcc.Input(id='in-yr', value='2011', type='number'),
                                        ], style={
                                            'font-size': 30,
                                            'height':'35px',
                                            'font-size':'30'}
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
    df_carrier_yr_delays = df_yr.groupby(['Month', 'Reporting_Airline'], as_index=False)\
        [['CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']]\
        .mean().reset_index()
    fig1 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='CarrierDelay',
                        color='Reporting_Airline',
                        title='Average Carrier Delay by Month per Airline')
    fig2 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='WeatherDelay',
                        color='Reporting_Airline',
                        title='Average Weather Delay by Month per Airline')
    fig3 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='NASDelay',
                        color='Reporting_Airline',
                        title='Average NAS Delay by Month per Airline')
    fig4 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='SecurityDelay',
                        color='Reporting_Airline',
                        title='Average Security Delay by Month per Airline') 
    fig5 = px.line(df_carrier_yr_delays, 
                        x='Month',
                        y='LateAircraftDelay',
                        color='Reporting_Airline',
                        title='Average Late Aircraft Delay by Month per Airline')                     
    return [fig1, fig2, fig3, fig4, fig5]


if __name__ == "__main__":
    app.run_server()