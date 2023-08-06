from plotly.missing_ipywidgets import FigureWidget


theme = "dark"


def get_stylesheet_path() -> str:
    return f"assets/{theme}.css"



def apply_figure_dark_theme(figure: FigureWidget):
    figure.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
    figure.update_layout(plot_bgcolor="rgba(0, 0, 0, 0)")
    figure.update_layout(font_color="#d8d4d0")
    figure.update_xaxes(linecolor="#d8d4d0")
    figure.update_yaxes(gridcolor="#d8d4d0")


def apply_figure_light_theme(figure: FigureWidget):
    figure.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
    figure.update_layout(plot_bgcolor="rgba(0, 0, 0, 0)")
    figure.update_layout(font_color="#33373e")
    figure.update_xaxes(linecolor="#33373e")
    figure.update_yaxes(gridcolor="#33373e")


def apply_figure_theme(figure: FigureWidget):
    if theme == "light":
        apply_figure_light_theme(figure)
    else:
        apply_figure_dark_theme(figure)



def get_data_table_header_dark_theme() -> dict:
    return {
        "backgroundColor": "rgba(0, 0, 0, 0)", 
        "border": "1px solid #d8d4d0",
        "textAlign": "left"
    }


def get_data_table_header_light_theme() -> dict:
    return {
        "backgroundColor": "rgba(0, 0, 0, 0)", 
        "border": "1px solid #33373e",
        "textAlign": "left"
    }


def get_data_table_header_theme() -> dict:
    if theme == "light":
        return get_data_table_header_light_theme()
    else:
        return get_data_table_header_dark_theme()



def get_data_table_cell_dark_theme() -> dict:
    return {
        "backgroundColor": "rgba(0, 0, 0, 0)", 
        "border": "1px solid #d8d4d0",
        "whiteSpace": "pre-line", 
        "textAlign": "left"
    }


def get_data_table_cell_light_theme() -> dict:
    return {
        "backgroundColor": "rgba(0, 0, 0, 0)", 
        "border": "1px solid #33373e",
        "whiteSpace": "pre-line", 
        "textAlign": "left"
    }


def get_data_table_cell_theme() -> dict:
    if theme == "light":
        return get_data_table_cell_light_theme()
    else:
        return get_data_table_cell_dark_theme()



def get_plot_colors() -> list:
    return ["#ff7d7d", "#ffc77d", "#fff47d", "#84de81", "#71d8e3", "#84ade8", "#dc8de3", 
        "#ffa47d", "#c1f07a", "#7fcdbb", "#b0acfc", "#d2acfa", "#f086d4", "#f582ac", 
        "#ffb8b8", "#f5ee9f", "#87e8b6", "#a6f6ff", "#b8d1f5", "#ebb6f0"]
