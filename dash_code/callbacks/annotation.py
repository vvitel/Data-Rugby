import time
from dash import callback, callback_context, Output, Input, State
from dash_code.repository.mongo import MongoDB

# Connection à la base de données
mongo = MongoDB()

# Annoter le match
@callback(
    [
        Output("store_annot", "data"),
        Output("alert_annot_add", "hide"),
        Output("alert_suppr_add", "hide"),
        Output("alert_send_data", "hide"),
        Output("card_penalty_precision", "style")
    ],
    [
        Input("btn_debmt1", "n_clicks"),
        Input("btn_finmt1", "n_clicks"),
        Input("btn_debmt2", "n_clicks"),
        Input("btn_finmt2", "n_clicks"),
        Input("btn_suppr", "n_clicks"),
        Input("btn_senddata", "n_clicks"),
        Input("btn_scrum_o_won", "n_clicks"),
        Input("btn_scrum_o_lose", "n_clicks"),
        Input("btn_scrum_o_stolen", "n_clicks"),
        Input("btn_lineout_o_won", "n_clicks"),
        Input("btn_lineout_o_lose", "n_clicks"),
        Input("btn_lineout_o_stolen", "n_clicks"),
        Input("btn_scrum_d_won", "n_clicks"),
        Input("btn_scrum_d_lose", "n_clicks"),
        Input("btn_scrum_d_stolen", "n_clicks"),
        Input("btn_lineout_d_won", "n_clicks"),
        Input("btn_lineout_d_lose", "n_clicks"),
        Input("btn_lineout_d_stolen", "n_clicks"),
        Input("btn_ets_try", "n_clicks"),
        Input("btn_ets_conversion_success", "n_clicks"),
        Input("btn_ets_conversion_fail", "n_clicks"),
        Input("btn_ets_penalty_success", "n_clicks"),
        Input("btn_ets_penalty_fail", "n_clicks"),
        Input("btn_ets_drop_success", "n_clicks"),
        Input("btn_ets_drop_fail", "n_clicks"),
        Input("btn_opponent_try", "n_clicks"),
        Input("btn_opponent_conversion_success", "n_clicks"),
        Input("btn_opponent_conversion_fail", "n_clicks"),
        Input("btn_opponent_penalty_success", "n_clicks"),
        Input("btn_opponent_penalty_fail", "n_clicks"),
        Input("btn_opponent_drop_success", "n_clicks"),
        Input("btn_opponent_drop_fail", "n_clicks"),
        Input("btn_penalty_for", "n_clicks"),
        Input("btn_penalty_against", "n_clicks"),
        Input("btn_penalty_ruck", "n_clicks"),
        Input("btn_penalty_scrum", "n_clicks"),
        Input("btn_penalty_lineout", "n_clicks"),
        Input("btn_penalty_tackle", "n_clicks"),
        Input("btn_penalty_offside", "n_clicks"),
        Input("btn_turnover_for", "n_clicks"),
        Input("btn_turnover_against", "n_clicks"),
        Input("btn_freekick_for", "n_clicks"),
        Input("btn_freekick_against", "n_clicks"),
        Input("btn_linebreak_for", "n_clicks"),
        Input("btn_linebreak_against", "n_clicks"),
        Input("btn_kick_for", "n_clicks"),
        Input("btn_kick_against", "n_clicks"),
        Input("btn_tackle_success", "n_clicks"),
        Input("btn_tackle_fail", "n_clicks")
    ],
    [State("input_namegame", "value"), State("store_annot", "data")],
)
def annotate_game(
    btn_debmt1,
    btn_finmt1,
    btn_debmt2,
    btn_finmt2,
    btn_suppr,
    btn_senddata,
    btn_scrum_o_won,
    btn_scrum_o_lose,
    btn_scrum_o_stolen,
    btn_lineout_o_won,
    btn_lineout_o_lose,
    btn_lineout_o_stolen,
    btn_scrum_d_won,
    btn_scrum_d_lose,
    btn_scrum_d_stolen,
    btn_lineout_d_won,
    btn_lineout_d_lose,
    btn_lineout_d_stolen,
    btn_ets_try,
    btn_ets_conversion_success,
    btn_ets_conversion_fail,
    btn_ets_penalty_success,
    btn_ets_penalty_fail,
    btn_ets_drop_success,
    btn_ets_drop_fail,
    btn_opponent_try,
    btn_opponent_conversion_success,
    btn_opponent_conversion_fail,
    btn_opponent_penalty_success,
    btn_opponent_penalty_fail,
    btn_opponent_drop_success,
    btn_opponent_drop_fail,
    btn_penalty_for,
    btn_penalty_against,
    btn_penalty_ruck,
    btn_penalty_scrum,
    btn_penalty_lineout,
    btn_penalty_tackle,
    btn_penalty_offside,
    btn_turnover_for,
    btn_turnover_against,
    btn_freekick_for,
    btn_freekick_against,
    btn_linebreak_for,
    btn_linebreak_against,
    btn_kick_for,
    btn_kick_against,
    btn_tackle_success,
    btn_tackle_fail,
    input_namegame,
    store_annot
):

    # Magie noire
    hide_add_alert, hide_suppr_alert, hide_send_data = True, True, True
    ctx = callback_context
    show_card_penalty = {"display": "none"}
    if not ctx.triggered:
        return store_annot, hide_add_alert, hide_suppr_alert, hide_send_data, show_card_penalty

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    data_annot = list(store_annot or [])
    now = time.time()

    # Dictionnaire des boutons et noms d'événements
    events = {
    "btn_debmt1": "debmt1",
    "btn_finmt1": "finmt1",
    "btn_debmt2": "debmt2",
    "btn_finmt2": "finmt2",
    "btn_scrum_o_won": "scrum_o_won",
    "btn_scrum_o_lose": "scrum_o_lose",
    "btn_scrum_o_stolen": "scrum_o_stolen",
    "btn_lineout_o_won": "lineout_o_won",
    "btn_lineout_o_lose": "lineout_o_lose",
    "btn_lineout_o_stolen": "lineout_o_stolen",
    "btn_scrum_d_won": "scrum_d_won",
    "btn_scrum_d_lose": "scrum_d_lose",
    "btn_scrum_d_stolen": "scrum_d_stolen",
    "btn_lineout_d_won": "lineout_d_won",
    "btn_lineout_d_lose": "lineout_d_lose",
    "btn_lineout_d_stolen": "lineout_d_stolen",
    "btn_ets_try": "ets_try",
    "btn_ets_conversion_success": "ets_conversion_success",
    "btn_ets_conversion_fail": "ets_conversion_fail",
    "btn_ets_penalty_success": "ets_penalty_success",
    "btn_ets_penalty_fail": "ets_penalty_fail",
    "btn_ets_drop_success": "ets_drop_success",
    "btn_ets_drop_fail": "ets_drop_fail",
    "btn_opponent_try": "opponent_try",
    "btn_opponent_conversion_success": "opponent_conversion_success",
    "btn_opponent_conversion_fail": "opponent_conversion_fail",
    "btn_opponent_penalty_success": "opponent_penalty_success",
    "btn_opponent_penalty_fail": "opponent_penalty_fail",
    "btn_opponent_drop_success": "opponent_drop_success",
    "btn_opponent_drop_fail": "opponent_drop_fail",
    "btn_penalty_for": "penalty_for",
    "btn_penalty_against": "penalty_against",
    "btn_turnover_for": "turnover_for",
    "btn_turnover_against": "turnover_against",
    "btn_freekick_for": "freekick_for",
    "btn_freekick_against": "freekick_against",
    "btn_linebreak_for": "linebreak_for",
    "btn_linebreak_against": "linebreak_against",
    "btn_kick_for": "kick_for",
    "btn_kick_against": "kick_against",
    "btn_tackle_success": "tackle_success",
    "btn_tackle_fail": "tackle_fail"
    }

    # Dictionnaire des boutons et noms d'événements pour les pénalités
    events_penalty = {
        "btn_penalty_ruck": "penalty_ruck",
        "btn_penalty_scrum": "penalty_scrum",
        "btn_penalty_lineout": "penalty_lineout",
        "btn_penalty_tackle": "penalty_tackle",
        "btn_penalty_offside": "penalty_offside"
        }

    # Ajouter une annotation
    if button_id in events:
        data_annot.append((events[button_id], now))
        hide_add_alert = False

    # Afficher la carte de précision des pénalités si pertinent
    if button_id in ["btn_penalty_for", "btn_penalty_against"]:
        show_card_penalty = {"display": "block"}
    
    # Annoter la raison de la pénalité
    if button_id in events_penalty:
        data_annot.append((events_penalty[button_id], now))
        hide_add_alert = False
        show_card_penalty = {"display": "none"}

    # Supprimer la dernière annotation
    elif button_id == "btn_suppr" and data_annot:
        data_annot.pop()
        hide_suppr_alert = False

    # Enregistrer dans la base de données
    elif button_id == "btn_senddata" and input_namegame:
        document_annot = {
            "date": time.strftime("%Y-%m-%d", time.localtime()).replace("-", "/"),
            "game": input_namegame,
            "annotations": data_annot,
        }
        mongo.collection_annotation.insert_one(document_annot)
        hide_send_data = False

        # Reset les annotations après envoi
        data_annot = []

    return data_annot, hide_add_alert, hide_suppr_alert, hide_send_data, show_card_penalty
