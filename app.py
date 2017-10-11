# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from guess_age import GuessAge

guessy = GuessAge()
app = dash.Dash()
server = app.server

markdown_text = '''
**Note**: This shows the probability distribution of age *conditional* on the provided name
(*i.e.*, the posterior distribution).
It does NOT provide any information about a name's absolute popularity. 
What it DOES show is a name's relative popularity across ages. 
Because this is a probability distribution, the area under the curve is 1 for every name.'''

app.layout = html.Div(children=[
    html.H1(children='How Old Is Your Name?'),

    html.Div(children='''
        Find the distribution of ages for any name.
    '''),

    dcc.Graph(id='example-graph'),

    dcc.RadioItems(
        id='input-sex',
        options=[{'label': 'Male', 'value': 'M'},
                 {'label': 'Female', 'value': 'F'}],
        value='M'
        ),

    dcc.Input(id='input-name', value='John', type="text"),

    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    html.Div([dcc.Markdown(children=markdown_text)])
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    state=[State('input-sex', 'value'),
           State('input-name', 'value')])
def update_fig(n_click, sex, raw_name):
    name = raw_name.lower()
    if ((sex == 'M' and name not in guessy.male_name_list) or
        (sex == 'F' and name not in guessy.female_name_list)):
        return {
            'layout': {
                'title': "Sorry, the database doesn't contain any {} named {}".
                          format('males' if sex == 'M' else 'females', name.title())
                }
            }
    else:
        df = guessy.p_yob_given_name(sex, name)
        df['age'] = df.yob.apply(lambda x: 2017-x)
        df.sort_values(['age'], inplace=True)

        return {
            'data': [go.Scatter(
                x=df['age'],
                y=df['p'],
                mode='lines',
                fill='tonexty'
                )],
            'layout': go.Layout(
                title='Age Distribution of {} Named {}'.
                       format('Males' if sex == 'M' else 'Females', name.title()),
                titlefont=dict(family='Arial, sans-serif', size=22),
                yaxis=dict(title='Probability',
                           titlefont=dict(family='Arial, sans-serif', size=15, color='grey')),
                xaxis=dict(title='Age',
                           titlefont=dict(family='Arial, sans-serif', size=15, color='grey'),
                           range=[1, 100],
                           dtick=5)
                )
            }

if __name__ == '__main__':
    app.run_server(debug=True)
