from dash import callback, Output, Input
from dash_code.repository.mongo import MongoDB

# Connection à la base de données
mongo = MongoDB()

# Mettre à jour les selects en fonction des sélections en cours - GPS
@callback(
    [Output("select_date", "data"),
     Output("select_match", "data"),
     Output("select_joueur", "data")],
    [Input("select_date", "value"),
     Input("select_match", "value"),
     Input("select_joueur", "value")],
    prevent_initial_call=True
)
def update_select(date, match, player):
    lst_date, lst_match, lst_player = mongo.find_gps_unique(date, match, player)
    return lst_date, lst_match, lst_player

# Mettre à jour les selects en fonction des sélections en cours - Video
@callback(
    [Output("select_date_video", "data"),
     Output("select_match_video", "data"),
     Output("select_joueur_video", "data")],
    [Input("select_date_video", "value"),
     Input("select_match_video", "value"),
     Input("select_joueur_video", "value")],
    prevent_initial_call=True
)
def update_select(date, match, player):
    lst_date, lst_match, lst_player = mongo.find_gps_unique(date, match, player)
    return lst_date, lst_match, lst_player
    
