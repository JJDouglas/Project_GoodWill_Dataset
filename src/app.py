from dash import Dash, dash_table, dcc, html, Input, Output
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import urllib.request


url = "https://projectgoodwilllink.s3.eu-south-1.amazonaws.com/Tab_macro.csv"
df = pd.read_csv(url)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "SOLVENCY II - MACRO DATASET"
server = app.server

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=100,
        style_table={"overflowX": "auto"},
        style_cell={'textAlign': 'left'},
        style_header={
            "fontWeight": "bold",
        },
    ),
    html.Div(id='datatable-interactivity-container'),
    html.A(
        'Download CSV',
        id='download-link',
        download="tab_macro.csv",
        href="",
        target="_blank",
        className="btn btn-primary"
    ),
])


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': "#0d6efd",
        "color": "white",
        "fontWeight": "Bold"
    } for i in selected_columns]


@app.callback(
    Output('download-link', 'href'),
    Input('download-link', 'n_clicks'),
    State('datatable-interactivity', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string


if __name__ == '__main__':
    app.run_server(debug=True)
