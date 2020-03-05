import dash_bootstrap_components as dbc
import dash_core_components as dcc

def Navbar():
    navbar = dbc.NavbarSimple(
        children = [
            dbc.NavItem(
                dbc.NavLink(
                    "About us",
                    href = "/about",
                    style = {
                        "float" : "left"
                    }
                )
            ),
            dbc.NavItem(
                dcc.Dropdown(
                    options = [
                        {"label" : "AAPL" , "value" : "AAPL"},
                        {"label" : "AMZN" , "value" : "AMZN"},
                        {"label" : "FB"   , "value" : "FB"  },
                        {"label" : "GOOG" , "value" : "GOOG"},
                        {"label" : "MSFT" , "value" : "MSFT"},
                        {"label" : "NFLX" , "value" : "NFLX"},
                        {"label" : "TSLA" , "value" : "TSLA"},
                        {"label" : "UBER" , "value" : "UBER"},
                    ],
                    placeholder = "Select Ticker",
                    multi = False,
                    style = {
                        "width" : "160%"
                    }
                )
            )
        ],
        brand = "Sentrade",
        brand_href = "/home",
        sticky = "top",
    )

    return navbar
        
