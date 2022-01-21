import dash  
import dash_bootstrap_components as dbc
from dash.long_callback import CeleryLongCallbackManager
from celery import Celery
import os
import redis

r = redis.from_url(os.environ.get("REDIS_URL"))
CELERY_BROKER_URL = os.environ.get("REDIS_URL")

celery_app = Celery(
    __name__, broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL
)
long_callback_manager = CeleryLongCallbackManager(celery_app)

# creating dash web app 
app = dash.Dash(__name__,
                long_callback_manager=long_callback_manager,
                title="COWID - a COVID-19 dashboard",
                suppress_callback_exceptions=True,
                meta_tags=[
                    # A description of the app, used by e.g.
                    # search engines when displaying search results.
                    {
                        'property': 'og:site_name',
                        'content': 'COWID - a COVID-19 dashboard',
                    },
                    {
                        'property': 'og:title',
                        'content': 'COWID - a COVID-19 dashboard',
                    },
                    {
                        'property': 'og:description',
                        'content': 'COWID - a COVID-19 dashboard',
                    },
                    {
                        'property': 'og:image',
                        'content': 'https://i.ibb.co/BfCMHLZ/logo-Tavola-disegno-1.png',
                    },
                  #set viewport for mobile
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                ],
                #import external stylesheets libraries
                external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'],
                )
