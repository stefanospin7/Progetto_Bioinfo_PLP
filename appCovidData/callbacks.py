import pandas as pd
import plotly.express as px
from appCovidData.app import app
from dash import Input, Output, State  # funzioni di layout html interattivo

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("fig-mondo", "figure"),
    Input("dato-input", "value"),
)
def update_figMondo(input_dato):
    df = pd.read_csv("data/owid-dataset.csv",
                     index_col="date",
                     parse_dates=["date"]
                     )
    df = df[df.location != 'World']
    df = df.groupby(['iso_code']).max()

    df = df.reset_index()
    figMondo = px.choropleth(df, locations="iso_code",
                             color=input_dato,
                             #  hover_name="location",
                             #  animation_frame="date",
                             #  title = "total_vaccinations_per_hundred",
                             # color_continuous_scale=px.colors.sequential.PuRd
                             )
    figMondo.update_layout(
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        showlegend=True
    )
    # fig["layout"].pop("updatemenus")
    # fig.show()
    return figMondo

