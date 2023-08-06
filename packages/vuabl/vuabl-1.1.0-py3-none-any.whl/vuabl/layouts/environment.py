from dash import html
from vuabl.data.environment import Environment



def generate_environment_layout(environment: Environment) -> html.Div:
    return html.Div([
        html.H1("Environment"),
        html.P(f"Layout path: {environment.layoutPath}"), 
        html.P(f"Unity Version: {environment.unityVersion}"), 
        html.P(f"Addressables Version: {environment.addressablesPackageVersion}")
    ])