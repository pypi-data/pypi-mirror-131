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
Rattail Commands
"""

from rattail import commands


class RunDashApp(commands.Subcommand):
    """
    Run a Dash web app
    """
    name = 'run-dashapp'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('--spec', default='rattail_dash.dashapp.sample:sample_dash_app',
                            help="The \"spec\" string for the Dash app to run. "
                            "This will normally be a factory function as opposed "
                            "to an app class.  If you do not specify this, the "
                            "default sample app will run, spec for which is: "
                            "rattail_dash.dashapp.sample:sample_dash_app")

    def run(self, args):
        factory = self.app.load_object(args.spec)
        dashapp = factory(self.config)
        dashapp.run_server(debug=True)
