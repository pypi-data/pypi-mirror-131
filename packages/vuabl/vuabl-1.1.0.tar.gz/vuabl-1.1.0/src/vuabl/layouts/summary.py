from dash import Dash, Output, Input, State, dcc, html
from dash.dependencies import Output, Input, State
from plotly.missing_ipywidgets import FigureWidget
from vuabl.data.build_layout import BuildLayout
from vuabl.data.size_plot_data import SizePlotData
import dash_bootstrap_components as dbc
import vuabl.data.size_plot_data as dtspd
import vuabl.plots.categories as pltcat
import vuabl.utils.conversion as conversion



def generate_summary_layout(buildLayout: BuildLayout) -> html.Div:
    categoriesData: SizePlotData = dtspd.get_build_categories_sizes_plot_data(buildLayout)
    
    elements: list = [
        html.P(f"Groups Count: {buildLayout.summary.groupsCount}"), 
        html.P(f"Total Build Size: {conversion.bytes_to_readable_size(buildLayout.summary.totalBuildSize)}"), 
        html.P(f"Total MonoScript Size: {conversion.bytes_to_readable_size(buildLayout.summary.totalMonoScriptSize)}"), 
        html.P(f"Total AssetBundle Object Size: {conversion.bytes_to_readable_size(buildLayout.summary.totalAssetBundleObjectSize)}")
    ]

    if not categoriesData.frame.empty:
        categoriesPie: FigureWidget = pltcat.plot_categories_sizes_pie(categoriesData)
        categoriesBars: FigureWidget = pltcat.plot_categories_sizes_bars(categoriesData)

        elements.append(dcc.Graph(figure=categoriesPie))
        elements.append(dcc.Graph(figure=categoriesBars))

    return html.Div([
        dbc.Button("Summary", className="collapse-button", id="summary-collapse-button", n_clicks=0), 
        dbc.Collapse(elements, className="collapse-body", id="summary-collapse", is_open=False)
    ], className="collapse-item")



def generate_summary_callbacks(app: Dash):
    @app.callback(
        Output("summary-collapse", "is_open"),
        Output("summary-collapse-button", "className"), 
        Input("summary-collapse-button", "n_clicks"), 
        State("summary-collapse", "is_open"), 
        State("summary-collapse-button", "className")
    )
    def toggle_summary_collapse(n: int, isOpen: bool, className: str):
        if n:
            isOpen = not isOpen

        if isOpen:
            className = className.replace(" collapsed", "")
        else:
            className = f"{className} collapsed"

        return isOpen, className