from ..app import app, db
from flask import render_template, request, flash, jsonify
from flask_login import login_required
from ..models.db_citynder import Commune, Etablissements_culturels
from sqlalchemy import func

@app.route("/graphiques/moyenne_loyer_par_commune", methods=['GET', 'POST'])
def graphique_loyer_par_commune():
    return render_template("pages/graphiques/moyenne_loyer_par_commune.html")

@app.route('/moyenne_loyer_par_commune_data', methods=['GET', 'POST'])
def moyenne_loyer_par_commune_data():
    communes = Commune.query.limit(35)
    data = []

    for commune in communes.all():
        loyer = (commune.LOYERM2_APPART + commune.LOYERM2_MAISON)/2
        data.append({
                'label': commune.LIBGEO,
                'nombre': loyer
        })


    return jsonify(data)
