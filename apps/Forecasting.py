import pandas as pd
import numpy as np
import pymc3 as pm
import arviz as az
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io
import scipy as sp

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_excel(DATA_PATH.joinpath('DeLorean Data Set.xlsx'))
impressions_forecast = az.from_netcdf(DATA_PATH.joinpath('Impressions Ratio.nc'))
engagement_forecast = az.from_netcdf(DATA_PATH.joinpath('Engagement Rate.nc'))
ctr_forecast = az.from_netcdf(DATA_PATH.joinpath('CTR.nc'))

df.drop('Unnamed: 0', axis = 1, inplace = True)

brand_unique = df['Brand'].unique()
brand = len(brand_unique)
brand_lookup = dict(zip(brand_unique, range(brand)))
brand_values = df['Brand'].replace(brand_lookup).values

client_unique = df['Client'].unique()
client = len(client_unique)
client_lookup = dict(zip(client_unique, range(client)))
client_values = df['Client'].replace(client_lookup).values

category_unique = df['Category'].unique()
category = len(category_unique)
category_lookup = dict(zip(category_unique, range(category)))
category_values = df['Category'].replace(category_lookup).values

platform_unique = df['Platform'].unique()
platform = len(platform_unique)
platform_lookup = dict(zip(platform_unique, range(platform)))
platform_values = df['Platform'].replace(platform_lookup).values

unit_unique = df['Ad Unit'].unique()
unit = len(unit_unique)
unit_lookup = dict(zip(unit_unique, range(unit)))
unit_values = df['Ad Unit'].replace(unit_lookup).values

tier_unique = df['Tier'].unique()
tier = len(tier_unique)
tier_lookup = dict(zip(tier_unique, range(tier)))
tier_values = df['Tier'].replace(tier_lookup).values

tier2_unique = df['Tier 2'].unique().tolist()
tier2 = len(tier2_unique)
tier2_lookup = dict(zip(tier2_unique, range(tier2)))
tier2_values = df['Tier 2'].replace(tier2_lookup).values
tier2_values = tier2_values.astype(int)
tier2_unique.sort(key=lambda x: (str(type(x)), x))

gender_unique = df['Gender**'].unique()
gender = len(gender_unique)
gender_lookup = dict(zip(gender_unique, range(gender)))
gender_values = df['Gender**'].replace(gender_lookup).values

ethnicity_unique = df['Ethnicity**'].unique()
ethnicity = len(ethnicity_unique)
ethnicity_lookup = dict(zip(ethnicity_unique, range(ethnicity)))
ethnicity_values = df['Ethnicity**'].replace(ethnicity_lookup).values

city_unique = df['Demo Top City'].unique()
city = len(city_unique)
city_lookup = dict(zip(city_unique, range(city)))
city_values = df['Demo Top City'].replace(city_lookup).values

state_unique = df['Demo Top State'].unique()
state = len(state_unique)
state_lookup = dict(zip(state_unique, range(state)))
state_values = df['Demo Top State'].replace(state_lookup).values

brand_cat_unique = df['Most Discussed Brand Category'].unique()
brand_cat = len(brand_cat_unique)
brand_cat_lookup = dict(zip(brand_cat_unique, range(brand_cat)))
brand_cat_values = df['Most Discussed Brand Category'].replace(brand_cat_lookup).values

layout = html.Div([
    html.Div([
        html.H1('Project DeLorean: Forecasting'),
        html.Div([
            html.Label('Brand: '),
            dcc.Dropdown(id = 'brand',
                        options = [{'label':i, 'value':i} for i in brand_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Client: '),
            dcc.Dropdown(id = 'client',
                        options = [{'label':i, 'value':i} for i in client_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Category: '),
            dcc.Dropdown(id = 'category',
                        options = [{'label':i, 'value':i} for i in category_unique])
            ]),
        html.Br(),
        html.Div([
        html.Label('Platform: '),
            dcc.Dropdown(id = 'platform',
                        options = [{'label':i, 'value':i} for i in platform_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Ad Unit: '),
            dcc.Dropdown(id = 'unit',
                        options = [{'label':i, 'value':i} for i in unit_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Follower Size Tier: '),
            dcc.Dropdown(id = 'tier',
                        options = [{'label':i, 'value':i} for i in tier2_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Gender: '),
            dcc.Dropdown(id = 'gender',
                        options = [{'label':i, 'value':i} for i in gender_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Ethnicity: '),
            dcc.Dropdown(id = 'ethnicity',
                        options = [{'label':i, 'value':i} for i in ethnicity_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('City: '),
            dcc.Dropdown(id = 'city',
                        options = [{'label':i, 'value':i} for i in city_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('State: '),
            dcc.Dropdown(id = 'state',
                        options = [{'label':i, 'value':i} for i in state_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Brand Category: '),
            dcc.Dropdown(id = 'brand_category',
                        options = [{'label':i, 'value':i} for i in brand_cat_unique])
            ]),
        html.Br(),
        html.Div([
            html.Label('Followers: '),
            html.Br(),
            dcc.Input(id = 'followers')
            ])
        ], style = {'width':'20%',
                    'top':'0'}
    ),
    html.Div([
        dcc.Graph(id = 'test_graph',
                 style = {'width':'80%', 
                          'float':'right', 
                          'position':'relative',
                          'top':'-1200px',
                          'z-index':'-1'}),
        dcc.Graph(id = 'test_graph2',
                 style = {'width':'80%', 
                          'float':'right', 
                          'position':'relative', 
                          'top':'-1150px',
                          'z-index':'-1'}),
        dcc.Graph(id = 'test_graph3',
                 style = {'width':'80%', 
                          'float':'right', 
                          'position':'relative', 
                          'top':'-1100px',
                          'z-index':'-1'})
    ])
], style = {'position':'absolute'})

@app.callback(
    [Output('test_graph', 'figure'),
     Output('test_graph2', 'figure'),
     Output('test_graph3', 'figure')],
    [Input('brand', 'value'),
     Input('client', 'value'),
     Input('category', 'value'),
     Input('platform', 'value'),
     Input('unit', 'value'),
     Input('tier', 'value'),
     Input('gender', 'value'),
     Input('ethnicity', 'value'),
     Input('city', 'value'),
     Input('state', 'value'),
     Input('brand_category', 'value'),
     Input('followers', 'value')]
)

def update_figure(brand, client, category, platform, unit, tier, gender, ethnicity, city, state, brand_category, followers):
    
    followers = float(followers)
    fig_data = (np.exp(impressions_forecast.posterior.a_intercept
        + impressions_forecast.posterior.b_1.sel({'Brand':brand})
        + impressions_forecast.posterior.b_2.sel({'Client':client})
        + impressions_forecast.posterior.b_3.sel({'Category':category})
        + impressions_forecast.posterior.b_4.sel({'Platform':platform})
        + impressions_forecast.posterior.b_5.sel({'Unit':unit})
        + impressions_forecast.posterior.b_6.sel({'Gender':gender})
        + impressions_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + impressions_forecast.posterior.b_8.sel({'Tier':tier})
        + impressions_forecast.posterior.b_9.sel({'City':city})
        + impressions_forecast.posterior.b_10.sel({'State':state})
        + impressions_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = 'chain') * followers)
    fig_data_mean = np.array(np.exp(impressions_forecast.posterior.a_intercept
        + impressions_forecast.posterior.b_1.sel({'Brand':brand})
        + impressions_forecast.posterior.b_2.sel({'Client':client})
        + impressions_forecast.posterior.b_3.sel({'Category':category})
        + impressions_forecast.posterior.b_4.sel({'Platform':platform})
        + impressions_forecast.posterior.b_5.sel({'Unit':unit})
        + impressions_forecast.posterior.b_6.sel({'Gender':gender})
        + impressions_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + impressions_forecast.posterior.b_8.sel({'Tier':tier})
        + impressions_forecast.posterior.b_9.sel({'City':city})
        + impressions_forecast.posterior.b_10.sel({'State':state})
        + impressions_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = ['chain', 'draw']) * followers).tolist()
    fig_data_5 = np.percentile(np.array(np.exp(impressions_forecast.posterior.a_intercept
        + impressions_forecast.posterior.b_1.sel({'Brand':brand})
        + impressions_forecast.posterior.b_2.sel({'Client':client})
        + impressions_forecast.posterior.b_3.sel({'Category':category})
        + impressions_forecast.posterior.b_4.sel({'Platform':platform})
        + impressions_forecast.posterior.b_5.sel({'Unit':unit})
        + impressions_forecast.posterior.b_6.sel({'Gender':gender})
        + impressions_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + impressions_forecast.posterior.b_8.sel({'Tier':tier})
        + impressions_forecast.posterior.b_9.sel({'City':city})
        + impressions_forecast.posterior.b_10.sel({'State':state})
        + impressions_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = ['chain']) * followers), 5).tolist()
    fig_data_95 = np.percentile(np.array(np.exp(impressions_forecast.posterior.a_intercept
        + impressions_forecast.posterior.b_1.sel({'Brand':brand})
        + impressions_forecast.posterior.b_2.sel({'Client':client})
        + impressions_forecast.posterior.b_3.sel({'Category':category})
        + impressions_forecast.posterior.b_4.sel({'Platform':platform})
        + impressions_forecast.posterior.b_5.sel({'Unit':unit})
        + impressions_forecast.posterior.b_6.sel({'Gender':gender})
        + impressions_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + impressions_forecast.posterior.b_8.sel({'Tier':tier})
        + impressions_forecast.posterior.b_9.sel({'City':city})
        + impressions_forecast.posterior.b_10.sel({'State':state})
        + impressions_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = ['chain']) * followers), 95).tolist()
    fig_data_list = [np.array(fig_data).tolist()]
    group_labels = ['Impressions']
    fig = ff.create_distplot(fig_data_list, group_labels, bin_size = 'auto')
    fig.add_vline(fig_data_mean, line_color = 'black', annotation_text = 'Mean: %.2f' % (fig_data_mean), annotation_yshift = 25)
    fig.add_vline(fig_data_5, line_color = 'grey', line_dash = 'dash', annotation_text = '5th Percentile: %.2f' % (fig_data_5), annotation_yshift = 50)
    fig.add_vline(fig_data_95, line_color = 'grey', line_dash = 'dash', annotation_text = '95th Percentile: %.2f' % (fig_data_95), annotation_yshift = 50)
    
    fig_data2 = np.exp(engagement_forecast.posterior.a_intercept
        + engagement_forecast.posterior.b_1.sel({'Brand':brand})
        + engagement_forecast.posterior.b_2.sel({'Client':client})
        + engagement_forecast.posterior.b_3.sel({'Category':category})
        + engagement_forecast.posterior.b_4.sel({'Platform':platform})
        + engagement_forecast.posterior.b_5.sel({'Unit':unit})
        + engagement_forecast.posterior.b_6.sel({'Gender':gender})
        + engagement_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + engagement_forecast.posterior.b_8.sel({'Tier':tier})
        + engagement_forecast.posterior.b_9.sel({'City':city})
        + engagement_forecast.posterior.b_10.sel({'State':state})
        + engagement_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                     ).mean(dim = 'chain') * 100
    fig_data2_mean = np.array(np.exp(engagement_forecast.posterior.a_intercept
        + engagement_forecast.posterior.b_1.sel({'Brand':brand})
        + engagement_forecast.posterior.b_2.sel({'Client':client})
        + engagement_forecast.posterior.b_3.sel({'Category':category})
        + engagement_forecast.posterior.b_4.sel({'Platform':platform})
        + engagement_forecast.posterior.b_5.sel({'Unit':unit})
        + engagement_forecast.posterior.b_6.sel({'Gender':gender})
        + engagement_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + engagement_forecast.posterior.b_8.sel({'Tier':tier})
        + engagement_forecast.posterior.b_9.sel({'City':city})
        + engagement_forecast.posterior.b_10.sel({'State':state})
        + engagement_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                     ).mean(dim = ['chain', 'draw']) * 100).tolist()
    fig_data2_5 = np.percentile(np.array(np.exp(engagement_forecast.posterior.a_intercept
        + engagement_forecast.posterior.b_1.sel({'Brand':brand})
        + engagement_forecast.posterior.b_2.sel({'Client':client})
        + engagement_forecast.posterior.b_3.sel({'Category':category})
        + engagement_forecast.posterior.b_4.sel({'Platform':platform})
        + engagement_forecast.posterior.b_5.sel({'Unit':unit})
        + engagement_forecast.posterior.b_6.sel({'Gender':gender})
        + engagement_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + engagement_forecast.posterior.b_8.sel({'Tier':tier})
        + engagement_forecast.posterior.b_9.sel({'City':city})
        + engagement_forecast.posterior.b_10.sel({'State':state})
        + engagement_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                     ).mean(dim = ['chain']) * 100), 5).tolist()
    fig_data2_95 = np.percentile(np.array(np.exp(engagement_forecast.posterior.a_intercept
        + engagement_forecast.posterior.b_1.sel({'Brand':brand})
        + engagement_forecast.posterior.b_2.sel({'Client':client})
        + engagement_forecast.posterior.b_3.sel({'Category':category})
        + engagement_forecast.posterior.b_4.sel({'Platform':platform})
        + engagement_forecast.posterior.b_5.sel({'Unit':unit})
        + engagement_forecast.posterior.b_6.sel({'Gender':gender})
        + engagement_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + engagement_forecast.posterior.b_8.sel({'Tier':tier})
        + engagement_forecast.posterior.b_9.sel({'City':city})
        + engagement_forecast.posterior.b_10.sel({'State':state})
        + engagement_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                     ).mean(dim = ['chain']) * 100), 95).tolist()
    fig_data2_list = [np.array(fig_data2).tolist()]
    group_labels2 = ['Engagement Rate']
    fig2 = ff.create_distplot(fig_data2_list, group_labels2, bin_size = 0.001,  colors = ['#E34A29'])
    fig2.add_vline(fig_data2_mean, line_color = 'black', annotation_text = 'Mean: %.2f' % (fig_data2_mean), annotation_yshift = 25)
    fig2.add_vline(fig_data2_5, line_color = 'grey', line_dash = 'dash', annotation_text = '5th Percentile: %.4f' % (fig_data2_5), annotation_yshift = 50)
    fig2.add_vline(fig_data2_95, line_color = 'grey', line_dash = 'dash', annotation_text = '95th Percentile: %.4f' % (fig_data2_95), annotation_yshift = 50)
    
    fig_data3 = np.exp(ctr_forecast.posterior.a_intercept
        + ctr_forecast.posterior.b_1.sel({'Brand':brand})
        + ctr_forecast.posterior.b_2.sel({'Client':client})
        + ctr_forecast.posterior.b_3.sel({'Category':category})
        + ctr_forecast.posterior.b_4.sel({'Platform':platform})
        + ctr_forecast.posterior.b_5.sel({'Unit':unit})
        + ctr_forecast.posterior.b_6.sel({'Gender':gender})
        + ctr_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + ctr_forecast.posterior.b_8.sel({'Tier':tier})
        + ctr_forecast.posterior.b_9.sel({'City':city})
        + ctr_forecast.posterior.b_10.sel({'State':state})
        + ctr_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = 'chain') * 100
    fig_data3_mean = np.array(np.exp(ctr_forecast.posterior.a_intercept
        + ctr_forecast.posterior.b_1.sel({'Brand':brand})
        + ctr_forecast.posterior.b_2.sel({'Client':client})
        + ctr_forecast.posterior.b_3.sel({'Category':category})
        + ctr_forecast.posterior.b_4.sel({'Platform':platform})
        + ctr_forecast.posterior.b_5.sel({'Unit':unit})
        + ctr_forecast.posterior.b_6.sel({'Gender':gender})
        + ctr_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + ctr_forecast.posterior.b_8.sel({'Tier':tier})
        + ctr_forecast.posterior.b_9.sel({'City':city})
        + ctr_forecast.posterior.b_10.sel({'State':state})
        + ctr_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = ['chain', 'draw']) * 100).tolist()
    fig_data3_5 = np.percentile(np.array(np.exp(ctr_forecast.posterior.a_intercept
        + ctr_forecast.posterior.b_1.sel({'Brand':brand})
        + ctr_forecast.posterior.b_2.sel({'Client':client})
        + ctr_forecast.posterior.b_3.sel({'Category':category})
        + ctr_forecast.posterior.b_4.sel({'Platform':platform})
        + ctr_forecast.posterior.b_5.sel({'Unit':unit})
        + ctr_forecast.posterior.b_6.sel({'Gender':gender})
        + ctr_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + ctr_forecast.posterior.b_8.sel({'Tier':tier})
        + ctr_forecast.posterior.b_9.sel({'City':city})
        + ctr_forecast.posterior.b_10.sel({'State':state})
        + ctr_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = ['chain']) * 100), 5).tolist()
    fig_data3_95 = np.percentile(np.array(np.exp(ctr_forecast.posterior.a_intercept
        + ctr_forecast.posterior.b_1.sel({'Brand':brand})
        + ctr_forecast.posterior.b_2.sel({'Client':client})
        + ctr_forecast.posterior.b_3.sel({'Category':category})
        + ctr_forecast.posterior.b_4.sel({'Platform':platform})
        + ctr_forecast.posterior.b_5.sel({'Unit':unit})
        + ctr_forecast.posterior.b_6.sel({'Gender':gender})
        + ctr_forecast.posterior.b_7.sel({'Ethnicity':ethnicity})
        + ctr_forecast.posterior.b_8.sel({'Tier':tier})
        + ctr_forecast.posterior.b_9.sel({'City':city})
        + ctr_forecast.posterior.b_10.sel({'State':state})
        + ctr_forecast.posterior.b_11.sel({'Brand Category':brand_category})
                      ).mean(dim = ['chain']) * 100), 95).tolist()
    fig_data3_list = [np.array(fig_data3).tolist()]
    group_labels3 = ['CTR']
    fig3 = ff.create_distplot(fig_data3_list, group_labels3, bin_size = 0.001,  colors = ['#258A09'])
    fig3.add_vline(fig_data3_mean, line_color = 'black', annotation_text = 'Mean: %.2f' % (fig_data3_mean), annotation_yshift = 25)
    fig3.add_vline(fig_data3_5, line_color = 'grey', line_dash = 'dash', annotation_text = '5th Percentile: %.4f' % (fig_data3_5), annotation_yshift = 50)
    fig3.add_vline(fig_data3_95, line_color = 'grey', line_dash = 'dash', annotation_text = '95th Percentile: %.4f' % (fig_data3_95), annotation_yshift = 50)
    
    return fig, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug = True, mode = 'external')
