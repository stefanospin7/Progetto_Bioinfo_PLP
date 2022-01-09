from appCovidData.app import app
from appCovidData.page_layouts.layout2 import make_layout as pag1
from dash import html, Input, Output, dcc  # funzioni di layout html interattivo

#creo un server dash 
server = app.server

#applico layout html
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children = pag1())
])

#run server 
if __name__ == '__main__':
    app.run_server(debug=True)
