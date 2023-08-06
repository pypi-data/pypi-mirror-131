from plotly.missing_ipywidgets import FigureWidget
from vuabl.data.size_plot_data import SizePlotData
import plotly.graph_objects as go
import vuabl.utils.theming as theming



def plot_categories_sizes_pie(data: SizePlotData) -> FigureWidget:
    figure: FigureWidget = go.Figure(go.Pie(
        labels=data.frame["category"], 
        values=data.frame["size"], 
        name=""))
    
    figure.update_layout(title_text=f"Size by category ({data.sizePostfix})")
    figure.update_traces(hovertemplate=f"Category: %{{label}}<br>Size: %{{value}}{data.sizePostfix}")
    figure.update_traces(marker_colors=theming.get_plot_colors())

    theming.apply_figure_theme(figure)

    return figure



def plot_categories_sizes_bars(data: SizePlotData) -> FigureWidget:
    figure: FigureWidget = go.Figure()
    colors: list[str] = theming.get_plot_colors()
    colorsCount: int = len(colors)

    for index, row in data.frame.iterrows():
        figure.add_trace(go.Bar(
            x=[row["category"]], 
            y=[row["size"]], 
            name=row["category"], 
            marker_color=colors[index % colorsCount]))

    figure.update_layout(title_text=f"Size by category ({data.sizePostfix})")
    figure.update_traces(hovertemplate=f"Category: %{{label}}<br>Size: %{{value}}{data.sizePostfix}")
    figure.update_traces(texttemplate=f"%{{y:.2f}}{data.sizePostfix}", textposition="auto")

    theming.apply_figure_theme(figure)

    return figure
