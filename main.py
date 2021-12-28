from appCovidData.app import app
from appCovidData.views.layout2 import make_layout as pag1
from appCovidData.views.layout3 import make_layout as pag2

from dash import html, Input, Output, dcc  # funzioni di layout html interattivo

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

if __name__ == '__main__':
    app.run_server(debug=True)