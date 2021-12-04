from my_dash_app.maindash import app
from my_dash_app.views.layout1 import make_layout
server = app.server

if __name__ == '__main__':
    app.layout = make_layout()
    app.run_server(debug=True)