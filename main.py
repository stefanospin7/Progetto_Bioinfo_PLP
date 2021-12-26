from my_dash_app.maindash import app
from my_dash_app.views.layout2 import make_layout as pag1
from my_dash_app.views.layout3 import make_layout as pag2
from dash import html, Input, Output, callback_context, State, dcc, dash  # funzioni di layout html interattivo

server = app.server
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update the index
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-2':
        return pag2()
    else:
        return pag1()
    # You could also return a 404 "URL not found" page here

#app.layout = make_layout()

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



if __name__ == '__main__':
    app.run_server(debug=True)