from dash_code.repository.mongo import MongoDB
from dash import Dash
from dash_code.layout import create_layout
from dash_code.callbacks import * 

# Connection à la base de données
mongo = MongoDB()

# Récupérer les informations pour les noms, dates, matchs
date_dic = [{"value": i['date'], "label": i['date']} for i in mongo.get_distinct_dates()]
match_dic = [{"value": i['game'], "label": i['game']} for i in mongo.get_distinct_matchs()]
joueur_dic = [{"value": i['player'], "label": i['player']} for i in mongo.get_distinct_players()]

# Création du front de l'app
front = create_layout(date_dic, match_dic, joueur_dic)

# Code de l'application
app = Dash(__name__)
server = app.server
app.layout = front

if __name__ == "__main__":
    app.run(debug=True)