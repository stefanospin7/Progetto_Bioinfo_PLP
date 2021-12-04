import dash  # layout html

app = dash.Dash(__name__,
                title="PLP Project 1 - Bioinformatica Tor Vergata",
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
                    {
                        'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0',
                    }
                ],
                )
