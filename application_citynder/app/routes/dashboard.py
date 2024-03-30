#import plotly.graph_objects as go
from ..app import app
from flask import render_template, jsonify, flash
from flask_login import login_required, current_user
from ..models.db_citynder import Commune, Utilisateurs
from sqlalchemy.sql import func


############################################## Route pour la carte du panier ############################################# 

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Route permettant l'affichage des cartes dans le dashboard.

    Returns
    -------
    template
        Retourne le template dashboard.html avec les communes présentes dans son panier.
    nbre_communes
        Retourne le nombre de communes dans le panier de l'utilisateur.
    """
    try:
        id = current_user.USER_ID
        nbre_communes = len(Commune.query.join(Utilisateurs.panier).filter(Utilisateurs.USER_ID==id).all())
    except Exception as e :
        nbre_communes=None
        flash("Une erreur s'est produite : "+ str(e))
    return render_template("/pages/dashboard.html", nbre_communes=nbre_communes)


@app.route("/carte_panier", methods=['GET'])
@login_required

#Récupère les données du panier par compte utilisateur 
def carte_panier():
    """
    Route permettant de récupérer les données du panier de l'utilisateur et les données de chaque 
    commune (coordonées géographiques, libéllé, région et prix du loyer). Stocke le résultat dans une liste.

    Returns
    -------
    json
        Retourne le json.
    """
    try:
        user_id = current_user.USER_ID

        communes = Commune.query.join(Utilisateurs.panier).filter(Utilisateurs.USER_ID == user_id).all()

        data = []

        for commune in communes:
            data.append({
                "label": commune.LIBGEO,
                "coord": {"lat": commune.LATITUDE, "long": commune.LONGITUDE},
                "region": commune.REGION,
                "loyer_maison": round(commune.LOYERM2_MAISON,2),
                "loyer_appart": round(commune.LOYERM2_APPART,2)
                })
            
    except Exception as e :
        flash("Une erreur s'est produite : "+ str(e))
    return jsonify(data)

############################################# Route pour le graphique top 30  ############################################# 

@app.route("/partials/graphiques/moyenne_loyer_par_commune", methods=['GET', 'POST'])
def graphique_loyer_par_commune():
    """
    Route permettant l'affichage du graphique loyer_par_commune.

    Returns
    -------
    template
        Retourne le template moyenne_loyer_par_commune.html.
    """
    return render_template("partials/graphiques/moyenne_loyer_par_commune.html")


@app.route('/moyenne_loyer_par_commune_data', methods=['GET'])
def moyenne_loyer_par_commune_data():
    """
    Route permettant de requêter les 30 communes les plus chères et stocke l'information (nom, prix du loyer) dans une liste .

    Returns
    -------
    json
        Retourne le json.
    """
    try:
        regions = Commune.query.with_entities(Commune.LIBGEO, func.avg((Commune.LOYERM2_APPART + Commune.LOYERM2_MAISON) / 2).label('nombre')).group_by(Commune.LIBGEO).all()

        regions_sorted = sorted(regions, key=lambda x: x[1], reverse=True)

        top_30_communes = regions_sorted[:30]

        data = [{'label': commune[0], 
                'nombre': round(commune[1], 2)} # pour réduire la décimale
                for commune in top_30_communes]
        
    except Exception as e :
        flash("L'affichage de la datavizualisation a rencontré une erreur : "+ str(e))
    return jsonify(data)

############################################# Route pour le graphique bottom 30 commune - ############################################# 

@app.route("/partials/graphiques/moyenne_loyer_par_commune_bottom", methods=['GET', 'POST'])
def graphique_loyer_par_commune_bottom():
    return render_template("partials/graphiques/moyenne_loyer_par_commune_bottom.html")

@app.route('/moyenne_loyer_par_commune_data_bottom_30', methods=['GET'])
def moyenne_loyer_par_commune_data_bottom_30():
    """
    Route permettant de requêter les 30 communes les moins chères et stocke l'information (nom, prix du loyer) dans une liste .

    Returns
    -------
    json
        Retourne le json.
    """
    try:
        regions = Commune.query.with_entities(Commune.LIBGEO, func.avg((Commune.LOYERM2_APPART + Commune.LOYERM2_MAISON) / 2).label('nombre')).group_by(Commune.LIBGEO).all()

        regions_sorted = sorted(regions, key=lambda x: x[1])

        bottom_30_communes = regions_sorted[:30]

        data = [{'label': commune[0], 
                'nombre': round(commune[1], 2)} 
                for commune in bottom_30_communes]
        
    except Exception as e :
        flash("L'affichage de la datavisualisation a rencontré une erreur : "+ str(e))

    return jsonify(data)

############################################# Route pour le graphique région ############################################# 

@app.route("/partials/graphiques/moyenne_loyer_par_region", methods=['GET', 'POST'])
def graphique_loyer_par_region():
    return render_template("partials/graphiques/moyenne_loyer_par_region.html")

@app.route('/moyenne_loyer_par_region_data', methods=['GET', 'POST']) 
def moyenne_loyer_par_region_data():  
    """
    Route permettant de requêter la moyenne du prix du loyer par égion et stocke l'information (nom, prix du loyer) dans une liste .

    Returns
    -------
    json
        Retourne le json.
    """
    try:
        regions = Commune.query.with_entities(Commune.REGION, func.avg((Commune.LOYERM2_APPART + Commune.LOYERM2_MAISON)/2)).group_by(Commune.REGION).all()
        
        data = []

        for region in regions:
            data.append({
                'label': region[0], 
                'nombre': round(region[1], 2)
            })

    except Exception as e :
        flash("L'affichage de la datavisualisation a rencontré une erreur : "+ str(e))
    return jsonify(data)


############################################## Route pour la heatmap (100 communes) ############################################# 
# Restée à l'état de brouillon

# @app.route("/carte_heatmap", methods=["GET"])
# @login_required
# def carte_heatmap():
#     communes_heatmap = Commune.query.all()

#     data_heat_map = []

#     for commune in communes_heatmap:
#         if commune.LOYERM2_APPART is not None:
#             data_heat_map.append([commune.INSEE_C, commune.LATITUDE, commune.LONGITUDE, commune.LOYERM2_APPART])
    
#     data_heat_map.sort(key=lambda x: x[3], reverse=True)

#     top_communes = data_heat_map[:100]

#     fig = go.Figure(go.Densitymapbox(
#         lat=[commune[1] for commune in top_communes],
#         lon=[commune[2] for commune in top_communes],
#         z=[commune[3] for commune in top_communes],
#         radius=10,
#         colorscale='hot',
#         colorbar=dict(title='Prix du loyer (€/m²)'),
#     ))

#     fig.update_layout(
#         mapbox_style="carto-positron",
#         mapbox_center_lon=2.454071,
#         mapbox_center_lat=46.603354, 
#         mapbox_zoom=4,
#     )

#     fig.update_layout(title='Heatmap des 100 communes aux loyers les plus chers de France (hors Mayotte)')

#     fig_json = fig.to_json()

#     return jsonify(fig_json)
