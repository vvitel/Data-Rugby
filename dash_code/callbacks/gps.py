import pandas as pd
from dash import callback, dcc, Output, Input, State
from dash_code.repository.mongo import MongoDB

# Connexion MongoDB
mongo = MongoDB()

# Constantes d'affichage
visible = {"display": "block"}
hidden = {"display": "none"}

# Définitions des fonctions
def get_documents(date, match, joueur):
    if joueur:
        documents = list(mongo.find_gps_by_player(joueur))
        if date:
            documents = [d for d in documents if d.get("date") == date]
        if match:
            documents = [d for d in documents if d.get("game") == match]
    elif date and match:
        documents = list(mongo.find_gps_by_date_and_match(date, match))
    else:
        documents = []
    return documents

def format_for_barplot_speeddistance(docus, choice):
    zones = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30"]
    formatted = []
    for doc in docus:
        dic = {"nom": doc[choice]}
        for i, zone in enumerate(zones):
            dic[zone] = round(doc["distance_zone"][i], 2)
        formatted.append(dic)
    return sorted(formatted, key=lambda x: sum(x[zone] for zone in zones), reverse=True)

def format_barplot(docus, choice_key, value_key, label, color):
    data = [{"nom": doc[choice_key], label: doc[value_key]} for doc in docus]
    data = sorted(data, key=lambda x: x[label], reverse=True)
    series = [{"name": label, "color": color}]
    return data, series

def format_for_scatter_speedaccel(docus, choice):
    lst_scatter = []
    lst_color = ["red.5", "pink.5", "grape.5", "violet.5", "indigo.5", "blue.5", "cyan.5",
                 "teal.5", "green.5", "lime.5", "yellow.5", "orange.5", "gray.5", "cyan.0"]
    for i, doc in enumerate(docus):
        name = doc[choice]
        max_speed = round(doc["vitesse"][0] * 3.6, 2)
        max_accel = round(doc["accel"][0], 2)
        lst_scatter.append({
            "color": lst_color[i % len(lst_color)],
            "name": name,
            "data": [{"vitesse": max_speed, "acceleration": max_accel}]
        })
    return lst_scatter

# Callbacks Dash
# Barplot - distance par zone de vitesse
@callback(
    [
        Output("barplot_dist", "data"),
        Output("barplot_dist", "dataKey"),
        Output("barplot_dist", "series"),
        Output("barplot_dist", "h"),
        Output("title_barplot", "style"),
        Output("barplot_dist", "style")
    ],
    [
        Input("select_date", "value"),
        Input("select_match", "value"),
        Input("select_joueur", "value")
    ],
    prevent_initial_call=True
)
def create_barplot_speeddistance(date, match, joueur):
    documents = get_documents(date, match, joueur)
    if not documents:
        return [], "", [], 0, hidden, hidden

    key = "game" if joueur else "player"
    lst_data = format_for_barplot_speeddistance(documents, key)
    height = max(400, 40 * len(lst_data))
    lst_color = [
        {"name": "0-5", "color": "violet.6"},
        {"name": "5-10", "color": "blue.6"},
        {"name": "10-15", "color": "teal.6"},
        {"name": "15-20", "color": "green.6"},
        {"name": "20-25", "color": "yellow.6"},
        {"name": "25-30", "color": "orange.6"}
    ]
    return lst_data, "nom", lst_color, height, visible, visible

# Scatterplot - vitesse / accélération
@callback(
    [
        Output("scatter_vitesse_accel", "data"),
        Output("scatter_vitesse_accel", "style"),
        Output("title_scatterspeedaccel", "style")
    ],
    [
        Input("select_date", "value"),
        Input("select_match", "value"),
        Input("select_joueur", "value")
    ],
    prevent_initial_call=True
)
def create_scatter_speedaccel(date, match, joueur):
    documents = get_documents(date, match, joueur)
    if not documents:
        return [], hidden, hidden

    key = "game" if joueur else "player"
    data = format_for_scatter_speedaccel(documents, key)
    return data, visible, visible

# Barplot - nombre d'accélérations
@callback(
    [
        Output("barplot_accel", "data"),
        Output("barplot_accel", "dataKey"),
        Output("barplot_accel", "series"),
        Output("title_nbaccel", "style"),
        Output("barplot_accel", "style")
    ],
    [
        Input("select_date", "value"),
        Input("select_match", "value"),
        Input("select_joueur", "value")
    ],
    prevent_initial_call=True
)
def create_barplot_accel(date, match, joueur):
    documents = get_documents(date, match, joueur)
    if not documents:
        return [], "nom", [], hidden, hidden

    key = "game" if joueur else "player"
    data, series = format_barplot(documents, key, "nb_acceleration", "nombre d'accélération", "violet.6")
    return data, "nom", series, visible, visible

# Barplot - nombre d'impacts
@callback(
    [
        Output("barplot_impact", "data"),
        Output("barplot_impact", "dataKey"),
        Output("barplot_impact", "series"),
        Output("title_nbimpact", "style"),
        Output("barplot_impact", "style")
    ],
    [
        Input("select_date", "value"),
        Input("select_match", "value"),
        Input("select_joueur", "value")
    ],
    prevent_initial_call=True
)
def create_barplot_impact(date, match, joueur):
    documents = get_documents(date, match, joueur)
    if not documents:
        return [], "nom", [], hidden, hidden

    key = "game" if joueur else "player"
    data, series = format_barplot(documents, key, "nb_impact", "nombre d'impact", "indigo.6")
    return data, "nom", series, visible, visible

# Donutchart - comparaison niveau international
@callback(
    [
        Output("donut_vmax", "data"),
        Output("donut_vmax", "style"),
        Output("donut_amax", "data"),
        Output("donut_amax", "style"),
        Output("title_donut", "style"),
    ],
    Input("select_joueur", "value"),
    prevent_initial_call=True,
)
def create_donutchart(joueur):
    if not joueur:
        return [], hidden, [], hidden, hidden
    if joueur:
        documents = get_documents(None, None, joueur)
        if not documents:
            return [], hidden, [], hidden, hidden

        # Obtenir valeurs maximales
        measured_vmax = max([doc["vitesse"][0] for doc in documents if doc["vitesse"]])
        measured_amax = max([doc["accel"][0] for doc in documents if doc["accel"]])

        # Calculer une note sur 100
        note_100_vmax = round(measured_vmax * 100 / 12.42, 1)
        note_100_amax = round(measured_amax * 100 / 9.5, 1)
        remainder_100_vmax = round(100 - note_100_vmax, 1)
        remainder_100_amax = round(100 - note_100_amax, 1)
        # Éléments à retourner
        data_donut_vmax = [
            {"name": "vmax mesurée", "value": note_100_vmax, "color": "indigo.4"},
            {"name": "vmax théorique", "value": remainder_100_vmax, "color": "gray.4"},
        ]
        data_donut_amax = [
            {"name": "vmax mesurée", "value": note_100_amax, "color": "indigo.4"},
            {"name": "vmax théorique", "value": remainder_100_amax, "color": "gray.4"},
        ]
        return data_donut_vmax, visible, data_donut_amax, visible, visible

# Télécharger les données
@callback(
    Output("download_data", "data"),
    [
        Input("btn_download_data", "n_clicks"),
        State("select_date", "value"),
        State("select_match", "value"),
        State("select_joueur", "value"),
    ],
    prevent_initial_call=True
)
def download_data(n_clicks, date, match, joueur):
    documents = get_documents(date, match, joueur)
    if not documents:
        return None
    df = pd.DataFrame(documents)
    return dcc.send_data_frame(df.to_csv, filename="data_RQ.csv", index=False)


    