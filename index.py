import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import Benchmarking, Forecasting

user_password_pairs = {'drew.shives@hellommc.com' : 'PASamuelson06171989#', 'alexandra.stevens@hellommc.com' : '240803', 'jomalley@hellommc.com' : 'MMC_830!'}

auth = dash_auth.BasicAuth(app, user_password_pairs)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Benchmarks|', href='/apps/Benchmarking'),
        dcc.Link('Forecasting', href='/apps/Forecasting'),
    ], className="row", style = {'position':'absolute', 'left':'100px'}),
    html.Br(),
    html.Div(id='page-content', children=[]),
    html.Br()
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Benchmarking':
        return Benchmarking.layout
    if pathname == '/apps/Forecasting':
        return Forecasting.layout
    else:
        return "Welcome to Project DeLorean! Please select a link above."


if __name__ == '__main__':
    app.run_server(debug=False)
