from dash import Dash, dcc, html, Input, Output, callback
from pages import neighborhood, neighborhood_recent, overview, recent, types_map, ncSumComp

external_stylesheets = ['/static/reports.css']
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server
available_dashboards = ["neighborhood", "neighborhood_recent", "overview", "recent", "types_map", "ncSumComp"]


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/neighborhood':
        return neighborhood.layout
    elif pathname == '/neighborhood_recent':
        return neighborhood_recent.layout
    elif pathname =='/overview':
        return overview.layout
    elif pathname =='/recent':
        return recent.layout
    elif pathname =='/types_map':
        return types_map.layout
    elif pathname == '/ncSumComp':
        return ncSumComp.layout
    else:
        return html.Div([
            dcc.Link(dashboard, href=f"/{dashboard}") for dashboard in available_dashboards 
        ], className='dash-links')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='5500', debug=True)