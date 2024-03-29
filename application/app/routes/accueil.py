from ..app import app, db
from flask import render_template
from sqlalchemy.sql import operators
# from ..models.citynder import 
from sqlalchemy.sql import text

@app.route("/")
@app.route("/accueil")
def accueil():
    return render_template("pages/accueil.html")

@app.route("/a_propos")
def a_propos():
    return render_template("pages/a_propos.html")
