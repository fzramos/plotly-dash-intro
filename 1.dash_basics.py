import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc

# Importing data from web location
# airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
#                             encoding = 'ISO-8859-1',
#                             dtype={'Div1Airport': str,
#                                     'Div1TailNum': str,
#                                     'Div2Airport': str,
#                                     'Div2TailNum': str})
# # Save the csv locally 
# airline_data.to_csv('./airline_data.csv')

# To speed up the application, use the following code after the csv has been downloaded from the weblocation
airline_data = pd.read_csv('./airline_data.csv',
                            encoding = 'ISO-8859-1',
                            dtype={'Div1Airport': str,
                                    'Div1TailNum': str,
                                    'Div2Airport': str,
                                    'Div2TailNum': str})

# Since the data is large, get a random sample
df = airline_data.sample(n=500, random_state=0)

# To look at the data, writing top 5 rows to a csv
df.head().to_csv('./df_head.csv')
# Displaying the data that will be graphed by the pie chart
print(df.groupby('DistanceGroup')['Flights'].sum())

# Using Plotly Express, create an interactive pie chart
# Power of Plotly: does the necessary group by and aggregation automatically
fig = px.pie(df, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

# If you'd like to see how the pie chart looks, 
# use the following 2 lines of code to show the pie chart in a web browser
# fig = px.pie(df, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')
# fig.show()

# Create a dash application
app = dash.Dash(__name__)

# Creating the layout and content for the application
# This is unique to Dash, no direct HTML code necessary for webpages
# HTML tags are abstracted as Dash Python classes
app.layout = html.Div(children=[html.H1('Airline Dashboard',
                                        style={'textAlign': 'center',
                                                'color': '#503D36',
                                                'font-size': 40}),
                                html.P('Proportion of distance group (250 mile distance interval group) by flights.',
                                        style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig),
                                ])

# Run the application
if __name__ == '__main__':
    app.run_server()
