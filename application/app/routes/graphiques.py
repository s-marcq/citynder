from ..app import app, db
from flask import render_template, request
from sqlalchemy import func, text
from ..models.db_citynder import Commune
from flask_login import login_required

@app.route("/graphiques/loyers_communes", methods=['GET', 'POST'])
def graphiques_loyers_communes():
    return render_template("pages/graphiques/loyers_communes.html")

@app.route("/graphiques/loyers_communes_data", methods=['GET', 'POST'])
def graphiques_loyers_communes_data():
    donnees_brutes = db.session.query(
    Commune.LIBGEO,
    func.avg(Commune.LOYERM2_MAISON).label('loyer_maison_moyen'),
    func.avg(Commune.LOYERM2_APPART).label('loyer_appart_moyen')
    )\
    .group_by(Commune.LIBGEO)\
    .order_by(func.avg(Commune.LOYERM2_APPART).desc())\
    .limit(20)


    donnees = []

    for commune in donnees_brutes.all():
        donnees.append({
            "label": commune[0].LIBGEO,
            "loyer": commune.LOYERM2_APPART
        })

    return donnees