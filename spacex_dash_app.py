#Install Libraries
#pip install pandas
#pip install dash
#pip install dash-html-components
#pip install dash-core-components
#pip install plotly


# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Create a list of options so I don't have to manually input it
# Get unique launch sites
unique_sites = spacex_df['Launch Site'].unique().tolist()
unique_sites.insert(0, 'ALL')  # Adding 'ALL' option
drop_options = [{'label': site, 'value': site} for site in unique_sites]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout

# Create an app layout
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40, 'height':'100%'}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                  dcc.Dropdown(id='site-dropdown',
                                        options=drop_options, #I made a unique list prior so I didn't enter them manually
                                        value='ALL',
                                        placeholder="Select a Launch Site",
                                        searchable=True
                                        ),
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
                                    marks={i: str(i) for i in range(0, 10001, 1000)},
                                    value=[min_payload, max_payload]
                                ),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
     Output(component_id='success-pie-chart', component_property='figure'),
     Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Get success counts for all sites
        success_counts = spacex_df[spacex_df['class'] == 1].groupby('Launch Site')['class'].count().reset_index(name='count')
        fig = px.pie(success_counts, values='count', names='Launch Site', title='Total Success Launches by Site')
    else:
        # Get success and failure counts for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index(name='count')
        success_counts.columns = ['class_status', 'count']
        success_counts['class_status'] = success_counts['class_status'].apply(lambda x: 'Success' if x == 1 else 'Failure')
        fig = px.pie(success_counts, values='count', names='class_status', title=f'Success Launches for {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Define the callback for TASK 4
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        title = f"Correlation between Payload and Success for {entered_site}"
    else:
        title = "Correlation between Payload and Success for all Sites"
        
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
