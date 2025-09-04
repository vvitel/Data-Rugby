import gzip
import json
import numpy as np

def get_data(source, debut, fin):
    """
    Lire le fichier contenant les données brutes au format json 
    in: chemin du fichier contenant les données, time stamp début et time stamp fin
    out: date, nom et 3 arrays contenant latitude, longitude, temps
    """
    # Ouvrir le fichier
    data = gzip.open(source, "rb").read()
    data = json.loads(data)
    debut, fin = debut - 14400, fin - 14400
    # Récupérer date et nom
    day = data["date"]
    user = data["user"]["name"]
    # Récupérer latitude, longitude et temps
    lst_time, lst_lat, lst_lon = [], [], []
    for i in range(len(data["gpss"])):
        if debut <= data["gpss"][i]["stamp"] <= fin:
            lst_time.append(data["gpss"][i]["stamp"])
            lst_lat.append(data["gpss"][i]["lat"])
            lst_lon.append(data["gpss"][i]["lon"])
    # Convertir en array numpy
    stamp, lat, lon = np.array(lst_time), np.array(lst_lat), np.array(lst_lon)
    return day, user, stamp, lat, lon
