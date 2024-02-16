from ..app import app, db
from flask import render_template, request, flash
from flask_login import login_required
# from ..models import
from sqlalchemy import func, text

@app.route("/resultats", methods=['GET', 'POST'])
def recap() :

    # bref récapitulatif du panier à intégrer à la page finale

    # try:
        # code recap du panier (requete panier utilisateur)
        # aller chercher les graphiques (à coder dans le dossier utils) réalisés sur les données et les renvoyer 
    
    # except Exception as e :
        # code s'il faut prévoir des exceptions
    return render_template("pages/???.html"
            # a completer
                )
