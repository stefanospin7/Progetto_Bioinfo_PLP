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
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_figMondo(input_dato, start_date, end_date):
    df = pd.read_csv("data/owid-dataset.csv",
                     parse_dates=["date"]
                     )
    df = df[df.location != 'World']
    periodo = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[periodo]

    df['date'] = df['date'].astype(str)

    figMondo = px.choropleth(df, locations="iso_code",
                             color=input_dato,
                             #  hover_name="location",
                             title = "input_dato",
                             # color_continuous_scale=px.colors.sequential.PuRd
                             animation_frame="date",
                             )
    figMondo.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    figMondo.update_layout(
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        showlegend=True
    )
    # fig["layout"].pop("updatemenus")
    # fig.show()
    return figMondo

