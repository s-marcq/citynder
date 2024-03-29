from ..app import app
from flask import render_template

@app.route("/")
@app.route("/accueil")
def accueil():
    """
    Route permettant l'affichage de la page d'accueuil

    Returns
    -------
    template
        Retourne le template de la page d'accueuil
    """
    return render_template("pages/accueil.html")

@app.route("/a_propos")
def a_propos():
    """
    Route permettant l'affichage de la page "à propos"

    Returns
    -------
    template
        Retourne le template de la page "à propos"
    """
    return render_template("pages/a_propos.html")
