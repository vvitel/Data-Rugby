import pandas as pd

#filtrer les données en fonction des sélections
def filter_dataframe(df, selected_date=None, selected_match=None, selected_name=None):
    #filtrer selon la date
    if selected_date:
        df = df[df["date"] == selected_date]
    #filtrer selon le match
    if selected_match:
        df = df[df["game"] == selected_match]
    #filtrer selon le nom
    if selected_name:
        df = df[df["player"] == selected_name]
    #réinitialiser index
    df = df.reset_index()
    return df