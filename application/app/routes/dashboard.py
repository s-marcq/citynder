import plotly.graph_objects as go
import numpy as np
from ..app import app, db
from flask import render_template, request, flash, jsonify
from flask_login import login_required, current_user, login_user
from ..models.db_citynder import Commune, Utilisateurs, contenu_paniers_utilisateurs
from sqlalchemy.sql import func

############################################# Route pour le graphique ############################################# 

@app.route("/graphiques/moyenne_loyer_par_region", methods=['GET', 'POST'])
def graphique_loyer_par_region():
    return render_template("pages/graphiques/moyenne_loyer_par_region.html")

@app.route('/moyenne_loyer_par_region_data', methods=['GET', 'POST']) 

#Récupère les régions et leur moyenne de loyer par mètre carré à partir de la base de données
def moyenne_loyer_par_region_data():  
    regions = Commune.query.with_entities(Commune.REGION, func.avg((Commune.LOYERM2_APPART + Commune.LOYERM2_MAISON)/2)).group_by(Commune.REGION).all()
    
    data = []

    for region in regions:
        data.append({
            'label': region[0], 
            'nombre': round(region[1], 2), # la moyenne de loyer arrondie à deux décimales
        })
    
    return jsonify(data)

############################################## Route pour la carte du panier ############################################# 

@app.route("/cartes/carte", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("/pages/dashboard.html")


@app.route("/carte_panier", methods=['GET'])
@login_required

#Récupère les données du panier par compte utilisateur 
def carte_panier():
    user_id = current_user.USER_ID

    communes = Commune.query.join(Utilisateurs.panier).filter(Utilisateurs.USER_ID == user_id).all()

    data = []

    for commune in communes:
        data.append({
            "label": commune.LIBGEO,
            "coord": {"lat": commune.LATITUDE, "long": commune.LONGITUDE},
            "region": commune.REGION,
            "loyer_maison": commune.LOYERM2_MAISON,
            "loyer_appart": commune.LOYERM2_APPART
            })

    return jsonify(data)

############################################## Route pour la heatmap ############################################# 
@app.route("/carte_heatmap", methods=["GET"])
@login_required
def carte_heatmap():
    communes_heatmap = Commune.query.all()

    data_heat_map = []

    for commune in communes_heatmap:
        if commune.LOYERM2_APPART is not None:
            data_heat_map.append([commune.INSEE_C, commune.LATITUDE, commune.LONGITUDE, commune.LOYERM2_APPART])
    
    data_heat_map.sort(key=lambda x: x[3], reverse=True)

    top_communes = data_heat_map[:100]

    fig = go.Figure(go.Densitymapbox(
        lat=[commune[1] for commune in top_communes],
        lon=[commune[2] for commune in top_communes],
        z=[commune[3] for commune in top_communes],
        radius=10,
        colorscale='hot',
        colorbar=dict(title='Prix du loyer (€/m²)'),
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center_lon=2.454071,
        mapbox_center_lat=46.603354, 
        mapbox_zoom=4,
    )

    fig.update_layout(title='Heatmap des communes aux loyers les plus chers en France')

    fig_json = fig.to_json()

    return jsonify(fig_json)
