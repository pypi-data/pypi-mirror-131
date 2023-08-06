from dash.dash_table import DataTable
from pandas import DataFrame
import vuabl.utils.conversion as conversion
import vuabl.utils.theming as theming


def create_group_assets_by_size_table(groupName, data: DataFrame) -> DataTable:
    groupID: str = conversion.to_layout_id(groupName)

    headerStyle: dict = theming.get_data_table_header_theme()
    cellStyle: dict = theming.get_data_table_cell_theme()

    return DataTable(
        id=f"group-{groupID}-assets-table", 
        data=data.to_dict("records"), 
        columns=[
            {"id": "number", "name": "№"}, 
            {"id": "path", "name": "Path"},  
            {"id": "type", "name": "Type"}, 
            {"id": "size", "name": "Size"}, 
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
                "border": "inherit !important",
            }
        ],
        editable=False, 
        cell_selectable=True
    )
