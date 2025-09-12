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
    ],
    [
        Input("btn_debmt1", "n_clicks"),
        Input("btn_debmt2", "n_clicks"),
        Input("btn_finmt1", "n_clicks"),
        Input("btn_finmt2", "n_clicks"),
        Input("btn_touche", "n_clicks"),
        Input("btn_melee", "n_clicks"),
        Input("btn_renvoi", "n_clicks"),
        Input("btn_essai", "n_clicks"),
        Input("btn_highlight", "n_clicks"),
        Input("btn_suppr", "n_clicks"),
        Input("btn_senddata", "n_clicks"),
    ],
    [State("input_namegame", "value"), State("store_annot", "data")],
)
def annotate_game(
    btn_debmt1,
    btn_debmt2,
    btn_finmt1,
    btn_finmt2,
    btn_touche,
    btn_melee,
    btn_renvoi,
    btn_essai,
    btn_highlight,
    btn_suppr,
    btn_senddata,
    input_namegame,
    store_annot,
):

    # Magie noire
    hide_add_alert, hide_suppr_alert, hide_send_data = True, True, True
    ctx = callback_context
    if not ctx.triggered:
        return store_annot, hide_add_alert, hide_suppr_alert, hide_send_data

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    data_annot = list(store_annot or [])
    now = time.time()

    # Dictionnaire des boutons et noms d'événements
    events = {
        "btn_debmt1": "debmt1",
        "btn_debmt2": "debmt2",
        "btn_finmt1": "finmt1",
        "btn_finmt2": "finmt2",
        "btn_touche": "touche",
        "btn_melee": "melee",
        "btn_renvoi": "renvoi",
        "btn_essai": "essai",
        "btn_highlight": "highlight",
    }

    # Ajouter une annotation
    if button_id in events:
        data_annot.append((events[button_id], now))
        hide_add_alert = False

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

    return data_annot, hide_add_alert, hide_suppr_alert, hide_send_data
