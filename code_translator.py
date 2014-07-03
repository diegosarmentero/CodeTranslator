# -*- coding: utf-8 -*-
#
# This file is part of Documentor
# (https://github.com/diegosarmentero/documentor).
#
# Documentor is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Documentor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Documentor; If not, see <http://www.gnu.org/licenses/>.

import os

import arguments
import code_parser


def execute_translator():
    """Run the commands selected by the user with CodeTranslator."""
    project, output = arguments.parse()
    output = os.path.abspath(output)

    if project:
        project = os.path.abspath(project)
        code_parser.create_po(project)

    #if project_to_translate:
        #project_to_translate = os.path.abspath(project_to_translate)
        #code_parser.translate_source(project_to_translate, output)
        #print("TRANSLATION GENERATED AT: %s" % output)

    if not project and not output:
        print("No arguments given, please run with -h argument")

if __name__ == '__main__':
    execute_translator()
