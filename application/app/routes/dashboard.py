from ..app import app, db
from flask import render_template, request, flash, jsonify
from flask_login import login_required, current_user, login_user
from ..models.db_citynder import Commune, Utilisateurs, contenu_paniers_utilisateurs
from sqlalchemy.sql import func

# @app.route("/graphiques/moyenne_loyer_par_commune", methods=['GET', 'POST'])
# def graphique_loyer_par_commune():
#     return render_template("pages/graphiques/moyenne_loyer_par_commune.html")

@app.route('/moyenne_loyer_par_commune_data', methods=['GET', 'POST'])
def moyenne_loyer_par_commune_data():
    communes = Commune.query.with_entities(Commune.REGION, func.avg((Commune.LOYERM2_APPART + Commune.LOYERM2_MAISON)/2)).group_by(Commune.REGION).all()
    print(communes)

    # group by region 
    # average de (commune.LOYERM2_APPART + commune.LOYERM2_MAISON)/2 (par commune)

    data = []

    for commune in communes:
        data.append({
                'label': commune[0],
                'nombre': commune[1]
        })


    return jsonify(data)

# Route pour la carte : va chercher les données du panier associé à un compte utilisateur


@app.route("/cartes/carte", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("/pages/dashboard.html")


@app.route("/carte_panier", methods=['GET'])
@login_required
def carte_panier():
    user_id = current_user.USER_ID
    communes = Commune.query.join(Utilisateurs.panier).filter(Utilisateurs.USER_ID == user_id).all()
    data = []

    for commune in communes:
        data.append({
            "label": commune.LIBGEO,
            "coord": {"lat": commune.LATITUDE, "long": commune.LONGITUDE}
        })

    return jsonify(data)

