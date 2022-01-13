from appCovidData.app import app
from appCovidData.page_layouts.layout2 import make_layout as pag1
from dash import html
from appCovidData import callbacks

# defining "server" variable as app's ".server" method return to make a connection with Gunicorn 
server = app.server

# applying html layout
app.layout = html.Div([
    html.Div(id='page-content', children = pag1())
])

#run server 
if __name__ == '__main__':
    app.run_server(debug=True)
