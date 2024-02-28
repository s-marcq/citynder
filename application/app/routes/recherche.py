from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort, session
import random
from sqlalchemy import or_
# from ..models.citynder import 
from ..models.formulaires import Recherche
from ..models.db_citynder import Commune, Environnement_naturel_specifique, Etablissements_culturels
from sqlalchemy.sql import text
from flask_login import login_required


@app.route("/recherche", methods=['GET', 'POST'])
def recherche():
    # coder des requêtes liées au formulaire de recherche (stocker les résultats sous forme de liste) -> Sarah et Anna
    query_results = Commune.query
    form = Recherche()

    try:
        
        if form.validate_on_submit():

            # Montagne
            session['montagne'] = request.form.get("montagne", None)
            if session['montagne']:
                query_results = query_results.join(Commune.environnement_naturel).filter(
                                Environnement_naturel_specifique.LOI_MONTAGNE == True,
                                Environnement_naturel_specifique.MASSIF != None
                            )
                
            
            # Culture
            session['musée'] =  request.form.get("musée", None)
            if session['musée'] :
                query_results = query_results.join(Commune.etablissements_culturels).filter(Etablissements_culturels.MUSEE_sum > 0)

            
            
            # Mettre les codes insee des résultats dans une liste, les mélanger et les mettre dans une variable de session
            liste_codes_insee = [resultat.INSEE_C for resultat in query_results]   
            liste_codes_insee = random.sample(liste_codes_insee, k=len(liste_codes_insee))
            session['resultats'] = liste_codes_insee
            session['index']= 0  
            print(session['resultats'])

            return redirect(url_for('profil_commune', index=session['index']))
        

        # récupérer les données de la session dans un dictionnaire pour préremplir le formulaire quand on fait un retour en arrière (voir l'attribut "value" dans les balises "input" du html)
        champs = {"montagne" : session.get('montagne'),
        "musée" : session.get('musée')
        }

    except Exception as e:
        flash("La recherche a rencontré une erreur "+ str(e), "info")
    
    return render_template('pages/recherche_filtres.html', form=form, champs = champs)



@app.route("/recherche_provisoire", methods=['GET'])
def recherche_provisoire():
    liste_provisoire = ["71155", "59350", "26333", "38349","75107", "71543", "12269"]
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
            # html : coder le bouton " voir le profil détaillé" qui assure la redirection vers cette route en transmettant la variable du code insee dans le template resultats.html

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




@app.route("/")
def route_test_bdd():
    test = Commune.query.filter(Commune.INSEE_C == 62765).first()
    print(test)
    print(f"Commune : {test}\n, Interet naturel : {test.environnement_naturel} \n culture : {test.etablissements_culturels} \n commerce : {test.equipements_commerciaux} \n sport : {test.equipements_sportifs}")
    return "ok"
