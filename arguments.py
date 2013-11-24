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

from __future__ import absolute_import

import argparse


usage = ("$documentor -p project_path -o output_path "
         "[--projectname name, --email address]")

epilog = ("This program comes with ABSOLUTELY NO WARRANTY."
          "This is free software, and you are welcome to redistribute "
          "it under certain conditions; for details see LICENSE.txt.")


def parse():
    """Parse the arguments received from the command line."""
    global usage
    global epilog
    project_to_po = None
    project_to_translate = None
    output = None

    try:
        parser = argparse.ArgumentParser(description=usage, epilog=epilog)

        parser.add_argument('-p', '--po', metavar='Project to PO', type=str,
            help='Read the source code of this project and generate po files',
            default=None)
        parser.add_argument('-t', '--translate', metavar='Translate Project',
            type=str, help='Source code to translate', default=None)
        parser.add_argument('-o', '--output', metavar='Output Folder', type=str,
            help='Place to locate the outpur result', default=".")

        opts = parser.parse_args()
        project_to_po = opts.po
        project_to_translate = opts.translate
        output = opts.output
    except Exception as reason:
        print("Args couldn't be parsed.")
        print(reason)
    return (project_to_po, project_to_translate, output)
