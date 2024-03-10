from ..app import app, db
from flask import render_template, request, flash
from flask_login import current_user, login_required
from ..models.db_citynder import Utilisateurs, Commune
# from ..models.formulaires import  



@app.route("/panier", methods=['GET', 'POST']) 
@app.route("/panier/<int:page>", methods=['GET', 'POST']) 
@login_required
def panier() :

    try:
        # code affichage du panier
        id = current_user.USER_ID
        if current_user.is_authenticated :
            communes = Commune.query.join(Utilisateurs.panier).filter(Utilisateurs.USER_ID==id).all()

        # gérer la pagination

        # code suppression d'un élément du panier
        # code mettre un élément en favori
    
    except Exception as e :
        flash("La recherche a rencontré une erreur : "+ str(e))
    return render_template("pages/panier.html", communes=communes)
