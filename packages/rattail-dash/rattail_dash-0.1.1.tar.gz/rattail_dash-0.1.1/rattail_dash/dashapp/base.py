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
Dash App "Base"
"""

import datetime

import dash
import pandas as pd


def make_basic_dash_app(config):
    """
    Make and return a simple Dash app.

    :param config: Rattail config object.
    """
    dashapp = dash.Dash(__name__)
    # dashapp.rattail_config = config
    return dashapp


def make_trainwreck_dataframe(config, date):
    """
    Make and return a simple dataframe for use with a Dash app,
    containing data from Trainwreck.

    :param date: Either a ``datetime.date`` object, or a string in
       YYYY-MM-DD format.
    """
    app = config.get_app()

    if not isinstance(date, datetime.date):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    start_time = datetime.datetime.combine(date, datetime.time(0))
    start_time = app.localtime(start_time)

    end_time = datetime.datetime.combine(date + datetime.timedelta(days=1),
                                         datetime.time(0))
    end_time = app.localtime(end_time)

    # TODO: maybe inspect date and use different year engine
    trainwreck_engine = config.trainwreck_engine

    # TODO: should transform timezone after fetch? this is surely quicker though
    df = pd.read_sql(
        """
        SELECT end_time AT TIME ZONE 'UTC' AT TIME ZONE %(timezone)s as end_time, 
                terminal_id, subtotal
        FROM transaction
        WHERE end_time >= %(start_time)s AT TIME ZONE 'UTC' AT TIME ZONE %(timezone)s
        AND end_time < %(end_time)s AT TIME ZONE 'UTC' AT TIME ZONE %(timezone)s
        ORDER BY end_time, terminal_id
        """,
        trainwreck_engine,
        params={'timezone': str(app.get_timezone()),
                'start_time': start_time,
                'end_time': end_time})

    return df
