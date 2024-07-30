# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label':'All Sites', 'value':'All Sites'},
                                        {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value':'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                    ],
                                    placeholder="Select a Launch Site Here",
                                    value='All Sites',
                                    searchable=True
                                )
                                ,
                                    
                                html.Br(),
                                
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, 
                                    max=10000, 
                                    step=1000,
                                    marks={i: '{}'.format(i) for i in range(0, 10001, 1000)},
                                    value=[min_payload, max_payload]
                                ),
                                #html.Div(id='output-container-range-slider'),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(launch_site):
    print(f"Entered site: {launch_site}")
    filtered_df = spacex_df
    if launch_site == 'All Sites':
        fig = px.pie(values=spacex_df.groupby('Launch Site')['class'].count(),
        names = spacex_df.groupby('Launch Site')['Launch Site'].first(),  
        title='Total Success Launches By Site')
        
        return fig
    else:
        fig = px.pie(values=spacex_df[spacex_df['Launch Site']==str(launch_site)]['class'].value_counts(normalize=True), 
                     names=spacex_df['class'].unique(), 
                     title='Total Success Launches for Site {}'.format(launch_site))
        
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider',component_property='value')])

def get_slider(entered_site, payload):
    filtered_df = spacex_df
    ccafs = filtered_df[filtered_df['Launch Site'] == 'CCAFS LC-40']
    vafb = filtered_df[filtered_df['Launch Site'] == 'VAFB SLC-4E']
    ksc = filtered_df[filtered_df['Launch Site'] == 'KSC LC-39A']
    ccafs_2 = filtered_df[filtered_df['Launch Site'] == 'CCAFS SLC-40']
    if entered_site == 'All Sites':
        fig = px.scatter(filtered_df[filtered_df['Payload Mass (kg)'].between(payload[0], payload[1])], 
        x='Payload Mass (kg)',y='class', 
        color="Booster Version Category" 
        )
        return fig
    else:
        if entered_site == 'CCAFS LC-40':
            fig = px.scatter(ccafs[ccafs['Payload Mass (kg)'].between(payload[0], payload[1])], 
            x='Payload Mass (kg)',y='class', 
            color="Booster Version Category")
            return fig
        elif entered_site == 'VAFB SLC-4E':
            fig = px.scatter(vafb[vafb['Payload Mass (kg)'].between(payload[0], payload[1])], 
            x='Payload Mass (kg)',y='class', 
            color="Booster Version Category")
            return fig
        elif entered_site == 'KSC LC-39A':
            fig = px.scatter(ksc[ksc['Payload Mass (kg)'].between(payload[0], payload[1])], 
            x='Payload Mass (kg)',y='class', 
            color="Booster Version Category")
            return fig
        elif entered_site == 'CCAFS SLC-40':
            fig = px.scatter(ccafs_2[ccafs_2['Payload Mass (kg)'].between(payload[0], payload[1])], 
            x='Payload Mass (kg)',y='class', 
            color="Booster Version Category")
            return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)