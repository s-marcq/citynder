from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort, session
import random
from sqlalchemy import or_, and_, func
from ..utils.calcul_loyer import calculer_loyer_m2_max, calculer_loyer_m2_min, normalisation_champs_texte
# from ..models.citynder import 
from ..models.formulaires import Recherche
from ..models.db_citynder import Commune, Environnement_naturel_specifique, Etablissements_culturels, Etablissements_commerciaux, Equipements_sportifs
from sqlalchemy.sql import text
from flask_login import login_required

@app.route("/")
@app.route("/accueil")
def accueil():
    test = Commune.query.join(Commune.equipements_commerciaux).filter((Etablissements_commerciaux.LOISIRS+Etablissements_commerciaux.STATION_SERVICE) ==17).first()
    print(f"Commune : {test}\n, Interet naturel : {test.environnement_naturel} \n culture : {test.etablissements_culturels} \n commerce : {test.equipements_commerciaux} \n sport : {test.equipements_sportifs}")
    return render_template("pages/accueil.html", test=test)
@app.route("/a_propos")
def a_propos():
    return render_template("pages/a_propos.html")
