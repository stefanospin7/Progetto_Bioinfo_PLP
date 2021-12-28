import dash  # layout html
import dash_bootstrap_components as dbc
from dash import html, Input, Output, callback_context

app = dash.Dash(__name__,
                title="PLP Project 1 - Bioinformatica Tor Vergata",
                suppress_callback_exceptions=True,
                meta_tags=[
                    # A description of the app, used by e.g.
                    # search engines when displaying search results.
                    {
                        'property': 'og:site_name',
                        'content': 'PLP Project 1 - Bioinformatica Tor Vergata',
                    },
                    # A description of the app, used by e.g.
                    # search engines when displaying search results.
                    {
                        'property': 'og:title',
                        'content': 'Progetto di analisi dati Covid-19 e Vaccinazioni',
                    },
                    # A description of the app, used by e.g.
                    # search engines when displaying search results.
                    {
                        'property': 'og:description',
                        'content': 'Progetto di analisi dati Covid-19 e Vaccinazioni',
                    },
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                ],
                external_stylesheets=[dbc.themes.FLATLY, dbc.icons.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'],
                )