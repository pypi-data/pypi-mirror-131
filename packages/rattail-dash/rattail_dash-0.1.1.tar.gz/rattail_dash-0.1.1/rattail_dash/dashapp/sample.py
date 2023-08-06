# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Sample Dash App
"""

import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from . import base


def sample_dash_app(config):
    """
    Make and return a "complete" sample Dash app.  Just for sake of a
    basic demo at this point.
    """
    app = config.get_app()
    dashapp = base.make_basic_dash_app(config)

    # colors = {
    #     # 'background': '#111111',
    #     'background': '#333333',
    #     'text': '#7FDBFF'
    # }

    # this date will be initially displayed, by default
    date = app.localtime().date()

    dashapp.layout = html.Div([
        html.H1("Hello {}".format(config.app_title()),
                style={
                    'textAlign': 'center',
                    # 'color': colors['text']
                }),

        html.Div([
            html.P([
                html.Span("""
                This is just a sample dashboard (feature preview) built
                with Dash + Rattail. (
                """),
                html.A('https://dash.plot.ly/', href='https://dash.plot.ly/'),
                html.Span(' )'),
            ],
                   # style={'color': colors['text']},
            ),
            html.P([
                html.Span("Below we are showing some transaction data from: "),
                # html.Span(app.render_date(date)),
                html.Span(id='current-date'),
            ]),
        ], style={'textAlign': 'center', 
                  # 'color': colors['text'],
        }),

        html.Div([
            dcc.DatePickerSingle(id='mydatepicker',
                             initial_visible_month=date,
                             date=date.strftime('%Y-%m-%d')),
        ], style={'textAlign': 'center'}),

        dcc.Graph(
            id='example-graph',
            figure=px.bar(),
        ),

        dcc.Graph(
            id='example-graph2',
            figure=px.line(),
        ),

    ], 
                              # style={'backgroundColor': colors['background']},
    )

    @dashapp.callback(Output('current-date', 'children'),
                      Input('mydatepicker', 'date'))
    def update_date_display(date):
        return date

    @dashapp.callback(Output('example-graph', 'figure'),
                      Output('example-graph2', 'figure'),
                      Input('mydatepicker', 'date'))
    def update_fig1(date):
        df = base.make_trainwreck_dataframe(config, date)
        
        fig = px.bar(df, x="terminal_id", y="subtotal",
                     barmode="group")

        fig2 = px.line(df, x='end_time', y='subtotal')

        return fig, fig2

    return dashapp
