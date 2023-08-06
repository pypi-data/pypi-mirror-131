from dash.dash_table import DataTable
from pandas import DataFrame
import vuabl.utils.theming as theming



def create_duplicates_table(data: DataFrame) -> DataTable:
    headerStyle: dict = theming.get_data_table_header_theme()
    cellStyle: dict = theming.get_data_table_cell_theme()

    return DataTable(
        id="duplicates-table", 
        data=data.to_dict("records"), 
        columns=[
            {"id": "number", "name": "№"}, 
            {"id": "path", "name": "Path"},  
            {"id": "size", "name": "Size"}, 
            {"id": "groups", "name": "Referenced By Groups"}, 
            {"id": "references", "name": "Referenced By Assets"}
        ], 
        page_size=25, 
        style_table={ "overflowX": "auto" }, 
        style_header=headerStyle, 
        style_cell=cellStyle, 
        style_data_conditional=[                
            {
                "if": {"state": "selected"},
                "backgroundColor": "inherit !important",
                "border": "inherit !important"
            }
        ],
        editable=False, 
        cell_selectable=True
    )
