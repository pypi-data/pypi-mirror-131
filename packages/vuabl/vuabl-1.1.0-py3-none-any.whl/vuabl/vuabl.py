from dash import Dash, html
from vuabl.data.build_layout import BuildLayout
from argparse import ArgumentParser, Namespace
import vuabl.parsing.build_layout as pblt
import vuabl.layouts.environment as ltenv
import vuabl.layouts.summary as ltsum
import vuabl.layouts.group as ltgr
import vuabl.layouts.assets as ltasts
import vuabl.utils.arguments as arguments
import vuabl.utils.theming as theming
import vuabl.utils.version as version
import os
import webbrowser



def run():
    argumentsParser: ArgumentParser = arguments.get_parser()
    argumentsValues: Namespace = argumentsParser.parse_args()

    if argumentsValues.version:
        print(version.get_version())
        return

    if not argumentsValues.path:
        print("You must provide a path to the build layout!")
        return

    theming.theme = argumentsValues.theme

    fullPath: str = os.path.abspath(argumentsValues.path)
    buildLayout: BuildLayout = pblt.read_build_layout(fullPath)

    app: Dash = Dash(__name__)
    app.title = f"Visualizer for Unity Addressables build layout ({version.get_version()})"

    app.layout = html.Div(children=[
        html.Link(rel="stylesheet", href=theming.get_stylesheet_path()), 
        ltenv.generate_environment_layout(buildLayout.environment), 
        ltsum.generate_summary_layout(buildLayout), 
        ltgr.generate_groups_layout(buildLayout.groups, buildLayout.assetsData), 
        ltasts.generate_assets_layout(buildLayout.assetsData)
    ])

    ltsum.generate_summary_callbacks(app)
    ltgr.generate_groups_callbacks(app, buildLayout.groups)
    ltasts.generate_assets_callbacks(app)

    if not argumentsValues.silent:
        webbrowser.open(f"http://{argumentsValues.address}:{argumentsValues.port}/")
    
    app.run_server(debug=argumentsValues.debug, host=argumentsValues.address, port=argumentsValues.port)
