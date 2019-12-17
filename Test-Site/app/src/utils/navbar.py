import dash_bootstrap_components as dbc
import dash_html_components as html


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

layout = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("VinHR TestSite", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            # href="https://plot.ly",
        ),

        dbc.Nav(
            [
                # dbc.NavLink("Home", href='/home-page'),
                dbc.NavLink("Model Test", href="/data-n-model-list"),
                # dbc.NavLink("Model Test", href="/model-test"),
                dbc.NavLink("Model Ranking List", href="/model-ranking"),
                dbc.NavLink("Help", href="/help"),
            ],
            pills=True,
        ),

    ],
    color="dark",
    dark=True,
    className='nav-bar'
)