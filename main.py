from my_dash_app.maindash import app
from my_dash_app.views.layout1 import make_layout

if __name__ == '__main__':
    app.layout = make_layout()
    server = app.server
    app.run_server(debug=True)