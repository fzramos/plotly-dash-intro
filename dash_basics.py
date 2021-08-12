import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc

# Importing data
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = 'ISO-8859-1',
                            dtype={'Div1Airport': str,
                                    'Div1TailNum': str,
                                    'Div2Airport': str,
                                    'Div2TailNum': str})

# Since the data is large, get a random sample
df = airline_data.sample(n=500, random_state=0)

# To look at the data, writing top 5 rows to a csv
df.head().to_csv('./df_head.csv')
# can see that the data isn't very clean, lots of nulls
print(df.groupby('DistanceGroup')['Flights'].sum())

# Using Plotly Express, create an interactive pie chart
px.pie(df, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

# If you'd like to see a pop-up of how the pie chart looks, use the following 2 lines of code
fig = px.pie(df, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')
fig.show()