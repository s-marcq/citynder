from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort, session
import random
from sqlalchemy import or_
# from ..models.citynder import 
#from ..models.formulaires import Recherche
from ..models.db_citynder import Commune
from sqlalchemy.sql import text
from flask_login import login_required

@app.route("/")
def route_test_bdd():
    test = Commune.query.filter(Commune.INSEE_C == 62765).first()
    print(f"Commune : {test}\n, Interet naturel : {test.environnement_naturel} \n culture : {test.etablissements_culturels} \n commerce : {test.equipements_commerciaux} \n sport : {test.equipements_sportifs}")
    return "ok" 

@app.route("/recherche_provisoire", methods=['GET'])
def recherche_provisoire():
    # code des requêtes liées au formulaire de recherche (stocker les résultats sous forme de liste) -> Sarah et Anna
    liste_provisoire = [71155, 59350, 26333, 38349,75107, 71543, 12269]
    liste_provisoire = random.sample(liste_provisoire, k=len(liste_provisoire))
    session['resultats'] = liste_provisoire
    session['index']= 0    
    return redirect(url_for('profil_commune', index=session['index']))


@app.route("/resultats/<int:index>") # MARINA
def profil_commune(index):
    """
    Route d'affichage des résultats. L'index correspond à l'index du résultat dans la liste transmise dans la route précédente
    L'index et la liste sont des variables de session propres à l'utilisateur.
    Lancer la route recherche provisoire est obligatoire avant de lancer cette route.
        => Prévoir une exception/redirection si elle n'a pas été lancée par l'utilisateur.
    """
    # try:
        # code affichage du profil  -> MARINA
            # stocker le résultat des requêtes dans un dico ou des variables puis l'afficher avec jinja en html
            # coder le bouton " voir le profil détaillé" qui assure la redirection vers cette route en transmettant la variable du code insee dans le template resultats.html

        # Pour plus tard : code ajout dans le panier, gérer le cas où il n'y a plus de résultats (peut-être à faire en amont ou en html)
    
    # except Exception as e :
        # gérer le cas où la liste est vide ou bien le cas où l'utilisatur n'est pas passé par la route /recherche
    return render_template("pages/resultats.html") # a completer

@app.route("/resultats/detail/<string:code_insee>") # GIL
def profil_detallé_commune(code_insee):
    """
    Route d'affichage des profils détaillés. Le code insee est une variable récupérée et transmise à l'url grâce au {{url_for()}} de jinja dans le template html quand on clique sur un bouton pour voir le profil détaillé.
    Faire des tests avec des codes insee au hasard en attendant que le bouton soit codé par Marina.
    Lancer la route précédente est obligatoire avant de lancer cette route.
        => Prévoir une exception/redirection si elle n'a pas été lancée par l'utilisateur.
    """
    # try:
        # code affichage du profil détaillé -> GIL
            # stocker le résultat des requêtes dans un dico ou des variables puis l'afficher avec jinja en html

    # except Exception as e :

    return render_template("pages/profil_detaille0.html" # a completer
                           )

@app.route("/suivant/<int:index>")
# coder en HTML/Jinja l'accès à cette route quand le bouton pour passer au résultat suivant est cliqué 
def page_suivante(index):
    # Passer à la page suivante
    session['index'] += 1
    return redirect(url_for('profil_commune', code_insee='', index=session['index']))

