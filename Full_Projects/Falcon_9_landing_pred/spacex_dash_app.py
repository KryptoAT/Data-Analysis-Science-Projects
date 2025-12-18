# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

file_path = r'C:\Users\brooksat\Documents\Data-Analysis-Science-Projects\Full_Projects\Falcon_9_landing_pred\dataset_p2.csv'
# Read the airline data into pandas dataframe
df_spacex = pd.read_csv(file_path)
max_payload = df_spacex['PayloadMass'].max()
#print(max_payload)
min_payload = df_spacex['PayloadMass'].min()


filtered_df = df_spacex.loc[df_spacex['PayloadMass'] >= 5000]

filtered_df.dtypes
#df_spacex.head()

#filtered_df = df_spacex.loc[df_spacex['Class'] == 1].groupby('LaunchSite')['Class'].value_counts().reset_index()
#print(filtered_df)

df_spacex['LaunchSite'].value_counts().index
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options= [
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCSFS SLC 40', 'value': 'CCSFS SLC 40'},
                                                 {'label': 'KSC LC 39A', 'value': 'KSC LC 39A'},
                                                 {'label': 'VAFB SLC 4E', 'value': 'VAFB SLC 4E'},
                                             ],
                                             value = 'ALL',
                                             placeholder = 'place holder here',
                                             searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=max_payload, step=1000,
                                                marks={0: '0', max_payload: str(max_payload)},
                                                value=[0, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = df_spacex.loc[df_spacex['Class'] == 1].groupby('LaunchSite')['Class'].value_counts().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df,
                     values='count', 
                     names='LaunchSite', 
                     title= 'Total Success by Launch Sites')
        return fig
    else:
        filtered_df = df_spacex.loc[df_spacex['LaunchSite'] == entered_site].groupby('LaunchSite')['Class'].value_counts().reset_index()
        fig = px.pie(filtered_df,
                     values='count', 
                     names='Class', 
                     title= f'Total Success by Launches for site {entered_site}')
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, payload):
    filtered_df = df_spacex.loc[(df_spacex['PayloadMass'] >= payload[0]) & (df_spacex['PayloadMass'] <= payload[1]) ]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
                         x = 'PayloadMass',
                         y = 'Class',
                         color = 'LaunchSite',
                         title = 'Success by Payload Mass for All Sites')
        return fig
    else:
        filtered_df = filtered_df.loc[filtered_df['LaunchSite'] == entered_site]
        fig = px.scatter(filtered_df, 
                         x = 'PayloadMass',
                         y = 'Class',
                         color = 'Orbit',
                         title = f'Success by Payload Mass for {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run()
