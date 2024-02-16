from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from sqlalchemy import or_
# from ..models.citynder import 
from ..models.formulaires import Recherche
from sqlalchemy.sql import text
from flask_login import login_required



@app.route("/recherche")
def recherche():
    # code des requêtes liées au formulaire de recherche --> stocker les résultats
    return render_template("pages/???.html" # a completer
                           )

@app.route("/recherche/<int:code_Insee>")
def profil_commune(code_Insee):
    # try:
        # code affichage du profil --> tout mettre dans un dictionnaire ?
        # code affichage du profil détaillé --> tout mettre dans un dictionnaire ?
        # code ajout dans le panier
        # gérer le cas où il n'y a plus de résultats (peut-être à faire en amont ou en html)
    
    # except Exception as e :
        # code s'il faut prévoir des exceptions
    return render_template("pages/???.html" # a completer
                           )

"""
->  Une inspiration de la part de chatgpt :
"""
# @app.route('/', methods=['GET', 'POST'])
# def critere_selection():
#     if request.method == 'POST':
#         # Traitement des critères sélectionnés par l'utilisateur
#         critere_population = request.form.get('population')
#         critere_nombre_sportifs = request.form.get('nombre_sportifs')
#         # Filtrer les communes en fonction des critères
#         communes_filtrees = Commune.query.filter(Commune.population > critere_population, Commune.nombre_sportifs > critere_nombre_sportifs).all()
#         if communes_filtrees:
#             # Stockage des communes filtrées dans la session
#             session['communes_filtrees'] = [commune.INSEE_C for commune in communes_filtrees]
#             # Redirection vers la première page de résultats de recherche
#             return redirect(url_for('recherche_communes', index=0))
#         else:
#             return render_template('aucun_resultat.html')
#     return render_template('critere_selection.html')

# @app.route('/recherche/<int:index>')
# def recherche_communes(index):
#     # Récupérer les communes filtrées de la session
#     communes_filtrees = session.get('communes_filtrees', [])
#     if communes_filtrees:
#         # Vérifier si index est valide
#         if 0 <= index < len(communes_filtrees):
#             # Sélectionner la commune correspondant à l'index
#             commune_selectionnee = Commune.query.filter_by(INSEE_C=communes_filtrees[index]).first()
#             return render_template('resultat_recherche.html', commune_selectionnee=commune_selectionnee, index=index, total=len(communes_filtrees))
#         else:
#             # Toutes les communes ont été parcourues
#             return render_template('fin_resultats.html')
#     else:
#         # Les critères de recherche ne sont pas définis
#         return redirect(url_for('critere_selection'))
