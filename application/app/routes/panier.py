from ..app import app, db
from flask import render_template, request, flash
# from ..models import 
# from ..models.formulaires import  



@app.route("/panier", methods=['GET', 'POST']) 
@app.route("/panier/<int:page>", methods=['GET', 'POST']) 
def panier() :
    # try:
        # code affichage du panier
        # code suppression d'un élément du panier
        # code mettre un élément en favori
    
    # except Exception as e :
        # code s'il faut prévoir des exceptions
    return render_template("pages/???.html"
            # a completer
                )
