from dash import Dash, Output, Input, State, html
from dash.dash_table import DataTable
from pandas import DataFrame
import dash_bootstrap_components as dbc
import vuabl.data.table_data as dttbl
import vuabl.tables.assets as tblasts



def generate_assets_layout(assetsData: dict) -> html.Div:
    elements: list = [html.H2("Duplicates:")]

    duplicatesTableData: DataFrame = dttbl.get_duplicates_table(assetsData)
    duplicatesTable: DataTable = tblasts.create_duplicates_table(duplicatesTableData)

    elements.append(duplicatesTable)

    return html.Div([
        dbc.Button("Assets", className="collapse-button", id="assets-collapse-button", n_clicks=0), 
        dbc.Collapse(elements, className="collapse-body", id="assets-collapse", is_open=False)
    ], className="collapse-item")



def generate_assets_callbacks(app: Dash):
    @app.callback(
        Output("assets-collapse", "is_open"),
        Output("assets-collapse-button", "className"), 
        Input("assets-collapse-button", "n_clicks"), 
        State("assets-collapse", "is_open"), 
        State("assets-collapse-button", "className")
    )
    def toggle_assets_collapse(n: int, isOpen: bool, className: str):
        if n:
            isOpen = not isOpen

        if isOpen:
            className = className.replace(" collapsed", "")
        else:
            className = f"{className} collapsed"

        return isOpen, className
