from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output
import pathlib
from app import app
from datetime import date

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_excel(DATA_PATH.joinpath("DeLorean Data Set - 04262021.xlsx"))
df.drop('Unnamed: 0', axis = 1, inplace = True)
df.drop('Unnamed: 0.1', axis = 1, inplace = True)
df[['Brand', 'Campaign', 'Tier 2', 'Platform', 'Ad Unit', 'Gender**', 'Ethnicity**', 'Demo Top City', 'Demo Top State', 'Most Discussed Brand Category']] = df[['Brand', 'Campaign', 'Tier 2', 'Platform', 'Ad Unit', 'Gender**', 'Ethnicity**', 'Demo Top City', 'Demo Top State', 'Most Discussed Brand Category']].fillna('N/A')
df_time = df.dropna(subset = ['Live Date'])

brand_index = df['Brand'].sort_values(ascending = True).unique()
campaign_index = df['Campaign'].sort_values(ascending = True).unique()
tier_index = df['Tier 2'].unique().tolist()
tier_index.sort(key=lambda x: (str(type(x)), x))
platform_index = df['Platform'].sort_values(ascending = True).unique()
unit_index = df['Ad Unit'].sort_values(ascending = True).unique()
gender_index = df['Gender**'].sort_values(ascending = True).unique()
ethnicity_index = df['Ethnicity**'].sort_values(ascending = True).unique()
top_city_index = df['Demo Top City'].sort_values(ascending = True).unique()
top_state_index = df['Demo Top State'].sort_values(ascending = True).unique()
brand_category_index = df['Most Discussed Brand Category'].sort_values(ascending = True).unique()

layout = html.Div([
        html.H1(children='Benchmarking', style={'color': '#B50000', 'fontSize': 30}),

        html.Div([
            dbc.Row([
                dbc.Col(html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4(children = 'Date Filter'),
                                html.Hr(),
                            dcc.DatePickerRange(
                                id = 'date_picker',
                                min_date_allowed= df_time['Live Date'].min(),
                                max_date_allowed= df_time['Live Date'].max(),
                                initial_visible_month = df_time['Live Date'].min(),
                                start_date = date(2020, 1, 1),
                                end_date = date(2020, 12, 31)
                                ),
                                html.Br(),
                                html.Br(),
                                html.H4(children='Client Filters'),
                                html.Hr(),
                                html.P('Brands'),
                                dcc.Dropdown(id = 'brand',
                                    options=[
                                        {'label': i, 'value': i} for i in brand_index 
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.P('Campaigns'),
                                dcc.Dropdown(id = 'campaign',
                                    options = [
                                        {'label': i, 'value': i} for i in campaign_index
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.Br(),
                                html.H4(children = 'Platform Filters'),
                                html.Hr(),
                                html.P('Platforms'),
                                dcc.Dropdown(id = 'platform',
                                    options= [
                                        {'label': i, 'value': i} for i in platform_index
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.P('Ad Unit'),
                                dcc.Dropdown(id = 'unit',
                                    options = [
                                        {'label': i, 'value': i} for i in unit_index
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.Br(),
                                html.H4(children = 'Influencer Filters'),
                                html.Hr(),
                                html.P('Follower Tiers'),
                                dcc.Dropdown(id = 'tier',
                                             options = [
                                                 {'label': i, 'value': i} for i in tier_index
                                             ],
                                             multi = True,
                                             clearable = True,
                                             searchable = True
                                ),
                                html.P('Gender'),
                                dcc.Dropdown(id = 'gender',
                                    options = [
                                        {'label': i, 'value': i} for i in gender_index
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.P('Ethnicity'),
                                dcc.Dropdown(id = 'ethnicity',
                                    options = [
                                        {'label': i, 'value': i} for i in ethnicity_index
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.Br(),
                                html.H4('Audience Filters'),
                                html.Hr(),
                                html.P('Demo Top City'),
                                dcc.Dropdown(id = 'city',
                                    options = [
                                        {'label': i, 'value': i} for i in top_city_index
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.P('Demo Top State'),
                                dcc.Dropdown(id = 'state',
                                    options = [
                                        {'label': i, 'value': i} for i in top_state_index
                                    ],
                                    multi = True,
                                    clearable = True
                                ),
                                html.P('Most Discussed Brand Category'),
                                dcc.Dropdown(id = 'brand_category',
                                    options = [
                                        {'label': i, 'value': i} for i in brand_category_index
                                    ],
                                    multi = True,
                                    clearable = True
                                )
                            ])
                        ])
                    ]
                ), md=3),
                # Col 1 End
                dbc.Col(html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Overall'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        html.Div(id = 'posts_card'),
                                        html.P('Total Posts', style = {'fontSize':10})
                                    ], outline = True, style = {'padding':5})
                                ], sm = 6),
                                dbc.Col([
                                    dbc.Card([
                                        html.Div(id = 'percent_card'),
                                        html.P('Percentage of Posts', style = {'fontSize':10})
                                    ], style = {'padding':5})
                                ], sm = 6)
                            ])
                        ], md = 4),
                        dbc.Col([
                                html.H3('Ethnicity'),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card([
                                            html.Div(id = 'ethnicity_card'),
                                            html.P('Posts by non-White Influencers', style={ 'fontSize': 10})
                                        ], style={'padding': 5})
                                    ], sm=6),
                                    dbc.Col([
                                        dbc.Card([
                                            html.Div(id = 'ethnicity_percent_card'),
                                            html.P('Percentage of Posts', style={ 'fontSize': 10})
                                        ], style={'padding': 5})
                                    ], sm=6),
                                ])
                        ], md = 4),
                        dbc.Col([
                                html.H3('Gender'),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card([
                                            html.Div(id = 'male_card'),
                                            html.P('Posts by Male Influencers', style={ 'fontSize': 10})
                                        ], style={'padding': 5})
                                    ], sm=6),
                                    dbc.Col([
                                        dbc.Card([
                                            html.Div(id = 'female_card'),
                                            html.P('Posts by Female Influencers', style={ 'fontSize': 10})
                                        ], style={'padding': 5})
                                    ], sm=6),
                                ])
                        ], md = 4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                                html.H3('Awareness'),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card([
                                            html.Div(id = 'followers_card'),
                                            html.P('Total followers', style={ 'fontSize': 10})
                                        ], style={'padding': 5})
                                    ], sm=6),
                                    dbc.Col([
                                        dbc.Card([
                                            html.Div(id = 'impressions_card'),
                                            html.P('Impressions', style={ 'fontSize': 10})
                                        ], style={'padding': 5})
                                    ], sm=6),
                                ])
                        ], md = 4),
                        dbc.Col([
                            html.H3('Engagement'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        html.Div(id = 'engagement_card'),
                                        html.P('Engagements', style={'fontSize': 10})
                                    ], style={'padding': 5})
                                ], sm=6),
                                dbc.Col([
                                    dbc.Card([
                                        html.Div(id = 'engagement_rate_card'),
                                        html.P('Engagement Rate', style={'fontSize': 10})
                                    ],style={'padding': 5})
                                ], sm=6),
                            ])
                        ], md=4),
                        dbc.Col([
                            html.H3('Conversion'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        html.Div(id = 'clicks_card'),
                                        html.P('Clicks', style={'fontSize': 10})
                                    ], style={'padding': 5})
                                ], sm=6),
                                dbc.Col([
                                    dbc.Card([
                                        html.Div(id = 'ctr_card'),
                                        html.P('CTR', style={'fontSize': 10})
                                    ], style={'padding': 5})
                                ], sm=6),
                            ])
                        ], md = 4)
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.H4(
                            'Engagements Over Time',
                            style = {
                                'fontSize':35
                            }
                        ),
                        dcc.Graph(
                            id = 'eng_time_graph',
                            style = {
                                'align':'center',
                                'width':'100%'
                            }
                        )
                    ], style = {
                        'textAlign':'center'
                    }
                    ),
                    html.Div([
                        dt.DataTable(id='table',
                                    columns=[{"name": i, "id": i} for i in df],
                                    page_size = 10,
                                    style_table = {'overflowX':'auto'},
                                    data=df.to_dict('records'),
				    export_format = 'xlsx')
                    ])
                ]), md=8),
                dbc.Col(html.Div(""), md=2)
            ])
        ], style={'padding': 5})
])

@app.callback(
    [Output('posts_card', 'children'),
     Output('percent_card', 'children'),
     Output('ethnicity_card', 'children'),
     Output('ethnicity_percent_card', 'children'),
     Output('male_card', 'children'),
     Output('female_card', 'children'),
     Output('followers_card', 'children'),
     Output('impressions_card', 'children'),
     Output('engagement_card', 'children'),
     Output('engagement_rate_card', 'children'),
     Output('clicks_card', 'children'),
     Output('ctr_card', 'children'),
     Output('eng_time_graph', 'figure'),
     Output('table', 'data')],
    [Input('date_picker', 'start_date'),
     Input('date_picker', 'end_date'),
     Input('brand','value'),
     Input('campaign', 'value'),
     Input('tier', 'value'),
     Input('platform', 'value'),
     Input('unit', 'value'),
     Input('gender', 'value'),
     Input('ethnicity', 'value'),
     Input('city', 'value'),
     Input('state', 'value'),
     Input('brand_category', 'value')]
)

def update(start_date, end_date, brand, campaign, tier, platform, unit, gender, ethnicity, city, state, brand_category):
    
    dff = df
    dff_total = df
    
    dict_for_df = {'Brand':brand, 'Campaign':campaign, 'Tier 2':tier, 'Platform':platform, 'Ad Unit':unit, 'Gender**':gender, 'Ethnicity**':ethnicity, 'Demo Top City':city, 'Demo Top State':state, 'Most Discussed Brand Category':brand_category}
    
    keys1 = []
    values1 = []
    for key, value in dict_for_df.items():
        if bool(value) == True:
            keys1.append(key)
            values1.append(value)
    for i, j in zip(keys1, values1):
        if keys1[0] == i:
            dff = df[df[i].isin(j)]
        else:
            dff = dff[dff[i].isin(j)]
            
    if start_date is not None: # add start time
        dff = dff[dff['Live Date'] >= start_date]
        dff_total = dff_total[dff_total['Live Date'] >= start_date]

    if end_date is not None: # add end time
        dff = dff[dff['Live Date'] <= end_date]
        dff_total = dff_total[dff_total['Live Date'] <= end_date]
    
    dff_grouped = dff.groupby('Influencer ID').mean()
    dff_time = dff.dropna(subset = ['Live Date'])
    dff_grouped_time = dff_time.groupby('Live Date').sum().reset_index()
    
    ethnicity = 0
    dff_eth = dff.dropna(subset = ['Ethnicity**'])
    for i in dff_eth['Ethnicity**']:
        if i != 'White':
            ethnicity += 1
            
    male = 0
    dff_male = dff.dropna(subset = ['Gender**'])
    for i in dff_male['Gender**']:
        if i == 'Male':
            male += 1
            
    female = 0
    dff_female = dff.dropna(subset = ['Gender**'])
    for i in dff_female['Gender**']:
        if i == 'Female':
            female += 1
    
    fig1 = px.bar(dff_grouped_time, x = 'Live Date', y = 'Engagements', color_discrete_sequence = ['#B50000'])
    
    card1 = '{:,}'.format(dff['Influencer ID'].count().astype(int))
    card2 = '{:.2%}'.format(dff['Influencer ID'].count()/dff_total['Influencer ID'].count())
    card3 = '{:,}'.format(ethnicity)
    card4 = '{:.2%}'.format(ethnicity/dff_total['Influencer ID'].count())
    card5 = '{:,}'.format(male)
    card6 = '{:,}'.format(female)
    card7 = '{:,}'.format(dff_grouped['Follower Count'].sum().astype(int))
    card8 = '{:,}'.format(dff['Impressions'].sum().astype(int))
    card9 = '{:,}'.format(dff['Engagements'].sum().astype(int))
    card10 = '{:.2%}'.format(dff['Engagements'].sum()/dff['Follower Count'].sum())
    card11 = '{:,}'.format(dff['Clicks'].sum().astype(int))
    card12 = '{:.2%}'.format(dff['Clicks'].sum()/dff['Impressions'].sum())
    
    return card1, card2, card3, card4, card5, card6, card7, card8, card9, card10, card11, card12, fig1, dff.to_dict('records')
