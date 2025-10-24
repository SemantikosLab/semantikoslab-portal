from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import datetime

# --- Thème Bootstrap Quartz (extérieur)
external_stylesheets = [dbc.themes.QUARTZ]
load_figure_template("quartz")

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "SemantikosLab Portal"

year = datetime.datetime.now().year

# --- Données du graphe ---
nodes = [
    {"data": {"id": "semantikos", "label": "SemantikosLab"}},
    {"data": {"id": "tarot", "label": "Tarot"}},
    {"data": {"id": "symboles", "label": "Symboles"}},
    {"data": {"id": "textes", "label": "Textes"}},
    {"data": {"id": "arch", "label": "Archétypes"}},
]

edges = [
    {"data": {"source": "semantikos", "target": "tarot"}},
    {"data": {"source": "semantikos", "target": "symboles"}},
    {"data": {"source": "semantikos", "target": "textes"}},
    {"data": {"source": "symboles", "target": "arch"}},
]

# --- Style du graphe ---
stylesheet = [
    {"selector": "node", "style": {
        "background-color": "#f6d776",
        "label": "data(label)",
        "color": "#fff9e8",
        "font-size": "13px",
        "width": 45,
        "height": 45,
        "text-halign": "center",
        "text-valign": "center",
        "text-outline-color": "#0a1222",
        "text-outline-width": 2,
        "transition-property": "width height background-color",
        "transition-duration": "2s"
    }},
    {"selector": "edge", "style": {
        "line-color": "#d6b85c",
        "width": 2,
        "opacity": 0.75
    }},
]

# --- Layout principal ---
app.layout = html.Div(
    style={
        "position": "relative",
        "minHeight": "100vh",
        "overflow": "hidden",
        "backgroundColor": "#0a1222"
    },
    children=[
        # --- Graphe décoratif ---
        cyto.Cytoscape(
            id="bg-graph",
            elements=nodes + edges,
            layout={"name": "circle"},
            stylesheet=stylesheet,
            minZoom=0.5,
            maxZoom=1.2,
            style={
                "width": "100%",
                "height": "100vh",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "zIndex": "0",
            },
        ),

        # --- Interval pour l’animation du graphe ---
        dcc.Interval(id="pulse", interval=6000, n_intervals=0),

        # --- Contenu principal (centré verticalement et horizontalement) ---
        html.Div(
            id="content",
            style={
                "position": "relative",
                "zIndex": "1",
                "height": "100vh",
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "textAlign": "center",
                "color": "#f5f3ea"
            },
            children=[
                dbc.Container([
                    html.H1("☽ SemantikosLab ☾",
                            className="fw-bold mb-3",
                            style={"letterSpacing": "1px"}),

                    html.P("Laboratoire d’exploration sémantique des traditions symboliques — textes fondateurs, Tarot, astrologie — à la croisée de la linguistique, de l’IA et de la civilisation.",
                           className="mb-5",
                           style={"maxWidth": "800px", "margin": "0 auto", "opacity": 0.9}),

                    # --- Carte plus petite, centrée ---
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("🔮 Tarot SemantikosLab", className="card-title mb-3 fw-bold"),
                            html.P("Application d’analyse sémantique et symbolique du Tarot de Rider–Waite. "
                                   "Exploration des réseaux lexicaux, archétypes et cooccurrences symboliques.",
                                   className="mb-3",
                                   style={"fontSize": "15px"}),

                            html.P("« Entre le mot et le symbole, une cartographie de la civilisation humaine et de la conscience se dessine. »",
                                   style={"fontStyle": "italic", "opacity": 0.9, "marginBottom": "20px"}),

                            dbc.Button(
                                "Ouvrir l’application",
                                href="https://tarot-semantikoslab.amandinevelt.fr",
                                target="_blank",
                                color="light",
                                className="fw-bold"
                            )
                        ]),
                        className="shadow-lg card-glass mx-auto",
                        style={
                            "maxWidth": "600px",
                            "backgroundColor": "rgba(255,255,255,0.05)",
                            "border": "1px solid rgba(255,215,0,0.2)",
                            "backdropFilter": "blur(8px)",
                        }
                    )
                ])
            ]
        )
    ]
)

# --- Animation "neural breathing" ---
@app.callback(
    Output("bg-graph", "layout"),
    Input("pulse", "n_intervals")
)
def update_layout(n):
    layout_type = "circle" if n % 2 == 0 else "concentric"
    return {
        "name": layout_type,
        "animate": True,
        "randomize": True,
        "animationDuration": 2000
    }

# --- Footer global ---
app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            body {{
                margin: 0;
                background-color: #0a1222;
                overflow: hidden;
                font-family: 'Inter', sans-serif;
            }}
            footer {{
                position: fixed;
                bottom: 15px;
                left: 0;
                width: 100%;
                color: #f5f3ea;
                text-align: center;
                font-size: 14px;
                opacity: 0.85;
                z-index: 9999;
                letter-spacing: 0.3px;
            }}
            footer:hover {{
                color: #e0c46c;
                transition: color 0.6s ease;
            }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>© {year} Amandine Velt — SemantikosLab</footer>
        {{%config%}}
        {{%scripts%}}
        {{%renderer%}}
    </body>
</html>
"""

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
