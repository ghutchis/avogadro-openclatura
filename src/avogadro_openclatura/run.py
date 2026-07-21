#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-openclatura/

"""Dispatch feature identifier to the appropriate handler."""

import json
import sys


def run(args):
    avo_input = json.load(sys.stdin)
    output = None

    match args.feature:
        case "name":
            from .naming import clatura_name
            output = clatura_name(avo_input)

    if output is not None:
        print(json.dumps(output))
