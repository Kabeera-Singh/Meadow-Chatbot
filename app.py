import agent
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
zero_shot_agent = agent.DatabaseAgent()

# Add a heading
heading = html.H1("Meadow Application", style={'text-align': 'center'})

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            heading,
            dcc.Textarea(id='chat-area', style={'width': '100%', 'height': '50vh'}, disabled=True)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='chat-input', type='text', placeholder='Type a message...', style={'width': '75%'}),
            dbc.Button('Send', id='send-button', color='primary', style={'width': '25%'})
        ])
    ]),
    html.Div(id='store-chat', style={'display': 'none'})  # hidden div to store the chat history
], fluid=True)

@app.callback(
    dash.dependencies.Output('chat-area', 'value'),
    dash.dependencies.Output('store-chat', 'children'),
    dash.dependencies.Input('send-button', 'n_clicks'),
    dash.dependencies.State('chat-input', 'value'),
    dash.dependencies.State('store-chat', 'children')
)
def update_chat(n_clicks, input_value, stored_chat):
    if n_clicks is not None:
        print(input_value)
        response = zero_shot_agent.query(input_value)['output']
        new_chat = f"{stored_chat}\nUser: {input_value}\nBot: {response}"
        return new_chat, new_chat
    else:
        return '', ''

if __name__ == '__main__':
    app.run_server(debug=True)