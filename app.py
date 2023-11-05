import agent
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions = True)

with open("dash_config.json") as json_file:
    styles = json.load(json_file)

HEADER_STYLE = styles["HEADER"]
SIDEBAR_STYLE = styles["SIDEBAR"]
CONTENT_STYLE = styles["CONTENT"]

server = app.server
zero_shot_agent = agent.DatabaseAgent()

header = html.H1("Meadow Application", style=HEADER_STYLE)

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Info", href="/info", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
store_chat = html.Div(id='store-chat', style={'display': 'none'}, children='')

app.layout = html.Div([dcc.Location(id="url"), content, header, sidebar, store_chat])  # Add store_chat here

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    pages_dict = {
        "/": app_page,
        "/info": info_page,
    }

    if pathname in list(pages_dict.keys()):
        return pages_dict[pathname]

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

info_page = html.Div([
html.H3("Cultivating Green Spaces: Transforming Lawns into Native Plant Gardens for Environmental Sustainability"),
html.Content("In recent years, the environmental movement has gained momentum, with individuals and communities becoming increasingly aware of the importance of sustainable living practices. One innovative approach to fostering environmental consciousness is the creation of this app designed to help people transform their traditional lawns into thriving native plant gardens. This transformative initiative not only enhances the aesthetic appeal of landscapes but also significantly contributes to environmental sustainability in several ways."),

html.H5("\n1. Biodiversity Preservation:"),
html.Content("Native plants are indigenous to a specific region, making them well-adapted to local environmental conditions. By cultivating native plant gardens, users contribute to the preservation of regional biodiversity. These plants provide essential habitats and food sources for local wildlife, including birds, insects, and small mammals. In turn, this helps restore natural ecosystems, promoting a healthier balance in local flora and fauna."),

html.H5("\n2. Water Conservation:"),
html.Content("Traditional lawns often require copious amounts of water to maintain their lush appearance. Native plants, however, have adapted to local climate conditions, reducing the need for excessive watering. Through the app, users can access valuable information on drought-resistant native plants suitable for their region. By transitioning to these plants, individuals significantly decrease water consumption, conserving this precious resource and alleviating pressure on local water supplies."),

html.H5("\n3. Soil Health and Fertility:"),
html.Content("Native plants typically require minimal fertilizers and pesticides, promoting healthier soil ecosystems. They have evolved symbiotic relationships with local microorganisms, enhancing soil fertility naturally. By replacing non-native species with indigenous plants, the app encourages users to adopt organic gardening practices, leading to improved soil quality and reduced chemical runoff, benefiting nearby water bodies."),

html.H5("\n4. Carbon Sequestration and Air Quality Improvement:"),
html.Content("Trees and native plants absorb carbon dioxide during photosynthesis, effectively acting as carbon sinks. By encouraging users to incorporate trees and shrubs into their gardens, the app promotes carbon sequestration, mitigating climate change impacts. Additionally, the increased green cover enhances oxygen production, purifying the air and creating a healthier environment for both humans and wildlife."),

html.H5("\nConclusion:"),
html.Content("Creating an app that guides people in transforming their lawns into native plant gardens represents a significant step towards environmental sustainability. By promoting biodiversity, conserving water, enhancing soil health, sequestering carbon, and fostering community engagement, this initiative contributes to a greener and more sustainable future. Empowering individuals with the knowledge and tools to make eco-conscious choices, the app not only transforms landscapes but also nurtures a collective ethos of environmental responsibility, inspiring positive change one garden at a time."),
], style={'text-align': 'center','whiteSpace': 'pre-wrap'})

app_page = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                header,
                dcc.Textarea(id='chat-area', style={'width': '100%', 'height': '50vh'}, disabled=True)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Input(id='chat-input', type='text', placeholder='Type a message...', style={'width': '75%'},autoComplete=False),
                dbc.Button('Send', id='send-button', color='primary', style={'width': '25%'})
            ])
        ])
    ])
])

@app.callback(
    dash.dependencies.Output('chat-area', 'value'),
    dash.dependencies.Output('store-chat', 'children'),
    dash.dependencies.Input('send-button', 'n_clicks'),
    dash.dependencies.State('chat-input', 'value'),
    dash.dependencies.State('store-chat', 'children'),
)
def update_chat(n_clicks, input_value, stored_chat):
    if n_clicks is None:
        prompt = "Bot: Hello and welcome to Native plant garden app, where you can design a native garden for your outdoor spaces. This could be to replace an existing front or back lawn, as well as to enhance any outdoor area with vibrant, eco-friendly native plants. \nTo start, please give us your location, as well as information about the space you would like to transform, and anything else you think would be helpful."
        return prompt,prompt
    if n_clicks is not None:
        print(input_value)
        response = zero_shot_agent.query(input_value)['output']
        new_chat = f"{stored_chat}\nUser: {input_value}\nBot: {response}" if stored_chat else f"User: {input_value}\nBot: {response}"
        return new_chat, new_chat
    else:
        return '', ''

if __name__ == '__main__':
    app.run_server(debug=True)
