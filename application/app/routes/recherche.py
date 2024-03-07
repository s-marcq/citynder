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


############################################### ----- SARAH & ANNA ----- ###########################################################################################


@app.route("/recherche", methods=['GET', 'POST'])
@login_required
def recherche():
    # coder des requêtes liées au formulaire de recherche (stocker les résultats sous forme de liste) -> Sarah et Anna
    query_results = Commune.query
    form = Recherche()

    try:
        
        if form.validate_on_submit() and form.validation():
            # Loyer
            session['appart'] = request.form.get('appartement', None)
            session['maison'] = request.form.get('maison', None)
            session['appart_et_maison'] = request.form.get('appart_et_maison', None)

            session['loyer_min'] = request.form.get('loyer_min', None)
            session['loyer_max'] = request.form.get('loyer_max', None)
            session['surface_min'] = request.form.get('surface_min', None)
            session['surface_max'] = request.form.get('surface_max', None)


            # calcul du loyer minimal et maximal à requêter d'après les informations remplies par l'utilisateur
            loyer_m2_min = calculer_loyer_m2_min(session['loyer_min'], session['loyer_max'], session['surface_min'], session['surface_max'])
            loyer_m2_max = calculer_loyer_m2_max(session['loyer_min'], session['loyer_max'], session['surface_min'], session['surface_max'])

            if session['appart'] :
                query_results = query_results.filter(and_(Commune.LOYERM2_APPART >= loyer_m2_min,
                                                            Commune.LOYERM2_APPART <= loyer_m2_max))
            elif session['maison'] :
                query_results = query_results.filter(and_(Commune.LOYERM2_MAISON >= loyer_m2_min,
                                                           Commune.LOYERM2_MAISON <= loyer_m2_max))
            elif session['appart_et_maison']:
                query_results = query_results.filter(or_(and_(Commune.LOYERM2_MAISON >= loyer_m2_min, Commune.LOYERM2_MAISON <= loyer_m2_max),
                                                        and_(Commune.LOYERM2_APPART >= loyer_m2_min, Commune.LOYERM2_APPART <= loyer_m2_max)))            
            
            # Nature
            session['littoral'] = request.form.get("littoral", None)
            if session['littoral']:
                query_results = query_results.join(Commune.environnement_naturel).filter(or_(
                                Environnement_naturel_specifique.MER == True,
                                Environnement_naturel_specifique.ESTUAIRE == True,
                                Environnement_naturel_specifique.LAC == True)
                            )
            session['montagne'] = request.form.get("montagne", None)
            if session['montagne']:
                query_results = query_results.join(Commune.environnement_naturel).filter(or_(
                                Environnement_naturel_specifique.LOI_MONTAGNE == True,
                                Environnement_naturel_specifique.MASSIF != None)
                            )
            session['PNR'] = request.form.get("PNR", None)
            if session['PNR']:
                query_results = query_results.join(Commune.environnement_naturel).filter(or_(
                                Environnement_naturel_specifique.PN_LIBGEO != None,
                                Environnement_naturel_specifique.PNR_LIBGEO != None)
                            )
                
            
            # Culture
            session['musée'] =  request.form.get("musée", None)
            if session['musée'] :
                query_results = query_results.join(Commune.etablissements_culturels).filter(Etablissements_culturels.MUSEE_sum > 0)

            session['opera'] =  request.form.get("opera", None)
            if session['opera'] :
                query_results = query_results.join(Commune.etablissements_culturels).filter(Etablissements_culturels.OPERA_sum > 0)
           
            session['cinema'] =  request.form.get("cinema", None)
            if session['cinema'] :
                query_results = query_results.join(Commune.etablissements_culturels).filter(Etablissements_culturels.CINEMA_sum > 0)

            session['theatre'] = request.form.get("theatre", None)
            if session['theatre'] :
                query_results = query_results.join(Commune.etablissements_culturels).filter(Etablissements_culturels.THEATRE_sum > 0)
            
            session['bibliothèque'] = request.form.get("bibliothèque", None)
            if session['bibliothèque'] :
                query_results = query_results.join(Commune.etablissements_culturels).filter(Etablissements_culturels.BIB_sum> 0)

            #Sports
            session['foot'] = request.form.get("foot", None)
            if session['foot']:
                query_results = query_results.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Terrain de football")

            session['piscine'] = request.form.get("piscine", None)
            if session['piscine']:
                query_results = query_results.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Piscine/Bassin exercice aquatique")

            session['rando'] = request.form.get("rando", None)
            if session['rando']:
                query_results = query_results.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Boucle de randonnée")

            session['sportco'] = request.form.get("sportco", None)
            if session['sportco']:
                query_results = query_results.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Salles de pratiques collectives / gymnase")

            session['escalade'] = request.form.get("escalade", None)
            if session['escalade']:
                query_results = query_results.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Equipement escalade")


            session['petanque'] = request.form.get("petanque", None)
            if session['petanque']:
                query_results = query_results.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Terrain de pétanque")

            # commerces 
            session['com_alim'] = request.form.get("com_alim", None)
            match session['com_alim']:
                case "0":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(Etablissements_commerciaux.ALIMENTATION == 0)
                case "1" :
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(Etablissements_commerciaux.ALIMENTATION == 1)

                case "2 à 5":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(and_(Etablissements_commerciaux.ALIMENTATION >= 2, Etablissements_commerciaux.ALIMENTATION <= 5))

                case "5 à 10":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(and_(Etablissements_commerciaux.ALIMENTATION >= 5, Etablissements_commerciaux.ALIMENTATION <= 10))

                    
                case "plus de 10":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(and_(Etablissements_commerciaux.ALIMENTATION > 10))
            
            session['com_non_alim'] = request.form.get("com_non_alim", None)
            commerces_non_alimentaires = Etablissements_commerciaux.LOISIRS + Etablissements_commerciaux.STATION_SERVICE + Etablissements_commerciaux.BEAUTE_ET_ACCESSOIRES + Etablissements_commerciaux.COMMERCES_GENERAUX +Etablissements_commerciaux.FLEURISTE_JARDINERIE_ANIMALERIE
            match session['com_non_alim']:
                case "0":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(commerces_non_alimentaires==0)

                case "1" :
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(commerces_non_alimentaires==1)

                case "2 à 5":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(and_(commerces_non_alimentaires>=2, commerces_non_alimentaires<=5))

                case "5 à 10":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(and_(commerces_non_alimentaires>=5, commerces_non_alimentaires<=10))

                    
                case "plus de 10":
                    query_results = query_results.join(Commune.equipements_commerciaux).filter(commerces_non_alimentaires>=10)

            # Population
            session['pop'] = request.form.get('pop', None)
            match session['pop']:
                case 'moins de 1 000':
                    query_results= query_results.filter(Commune.POP <= 1000)
                case '1 000 à 5 000':
                    query_results = query_results.filter(and_(Commune.POP > 1000, Commune.POP<=5000))
                case '5 000 à 10 000':
                    query_results = query_results.filter(and_(Commune.POP > 5000, Commune.POP<=10000))
                case 'plus de 10 000':
                    query_results = query_results.filter(Commune.POP > 10000)

            # # Département 
            #         """pour l'instant une seule possibilité à cocher, transformer en plusieurs options"""
            # session['departement'] = request.form.get("departement", None)
            # if session['departement'] :
            #     query_results  = query_results.filter(Commune.DEPARTEMENT == session['departement'])

            # # Région
            # if session['region'] :
            #     """pour l'instant une seule possibilité à cocher, transformer en plusieurs options"""
            #     query_results = query_results.filter(Commune.REGION == session['region'])

            # Mettre les codes insee des résultats dans une liste, les mélanger et les mettre dans une variable de session
            liste_codes_insee = [resultat.INSEE_C for resultat in query_results] 
 
            if liste_codes_insee == []: # cas où il n'y aurait pas de résultat 
                flash("Aucun résultat, veuillez réessayer")
                return redirect(url_for('recherche'))
            liste_codes_insee = random.sample(liste_codes_insee, k=len(liste_codes_insee))
            session['resultats'] = liste_codes_insee
            session['index']= 0  

            #for resultat in liste_codes_insee :
            resultat = Commune.query.filter(Commune.INSEE_C == session['resultats'][0]).first()
            print(resultat)
            return redirect(url_for('profil_commune', index=session['index']))

    
    except Exception as e:
        flash("La recherche a rencontré une erreur : "+ str(e))
    
    # sauvegarde des champs dans la session
    champs = {"montagne" : session.get('montagne'),
        "littoral" : session.get('littoral'),
        "PNR" : session.get('PNR'),
        "musée" : session.get('musée'),
        "opera" : session.get('opera'),
        "cinema" : session.get('cinema'),
        "theatre" : session.get('theatre'),
        "bibliothèque" : session.get('bibliothèque'),
        "foot" : session.get('foot'),
        "piscine" : session.get('piscine'),
        "rando" : session.get('rando'),
        "sportco" : session.get('sportco'),
        "escalade" : session.get('escalade'),
        "petanque" : session.get('petanque'),
        "appart" : session.get('appart'), 
        "maison" : session.get('maison'),
        "pop" : session.get('pop'),
        # "region" : session.get('region'),
        # "departement" : session.get('departement'),
        "appart_et_maison" : session.get('appart_et_maison'),
        "loyer_min" : normalisation_champs_texte(session.get('loyer_min')),
        "loyer_max" : normalisation_champs_texte(session.get('loyer_max')),
        "surface_min" : normalisation_champs_texte(session.get('surface_min')),
        "surface_max" : normalisation_champs_texte(session.get('surface_max'))
        }
    for champ in champs :
        if champs[champ]=="on":
            champs[champ]= "checked"

    return render_template('pages/recherche_filtres.html', form=form, champs=champs)

############################################## ----- RECHERCHE PROVISOIRE ----- ###############################################################################


# @app.route("/recherche_provisoire", methods=['GET'])
# def recherche_provisoire():
#     liste_provisoire = ["71155", "59350", "26333", "38349","75107", "71543", "12269"]
#     liste_provisoire = random.sample(liste_provisoire, k=len(liste_provisoire))
#     session['resultats'] = liste_provisoire
#     session['index']= 0    
#     return redirect(url_for('profil_commune', index=session['index']))


############################################### ----- MARINA ----- ###########################################################################################


"""
    Route qui affiche les résultats. L'index correspond à l'index du résultat dans la liste transmise dans la route précédente
    L'index et la liste sont des variables de session propres à l'utilisateur.
    Lancer la route recherche provisoire est obligatoire avant de lancer cette route.
        => Prévoir une exception/redirection si elle n'a pas été lancée par l'utilisateur.
"""
@app.route("/resultats/<int:index>")
@login_required
def profil_commune(index):
    try:
        # Récupérer la liste des codes INSEE des communes de la session
        liste_code_insee = session['resultats']

         # Vérifier si l'index est validé, s'il n'est pas vide ou trop plein, supérieur à la liste totale des codes insee
        if index < 0 or index >= len(liste_code_insee):
            raise IndexError("Index n'est pas valide.")
        
        # Récupérer le code INSEE de la commune à partir de l'index
        code_insee = liste_code_insee[index]

        # Récupérer les informations de base de la commune à partir de la bdd
        commune = Commune.query.get(code_insee)

        # Stocker le résultat des requêtes dans un dictionnaire pour les transmettre au template
        infos_commune = { 
            'code_insee': code_insee,
            'nom_commune': commune.LIBGEO,
            'prix_m2_maisons': commune.LOYERM2_MAISON,
            'prix_m2_appartements': commune.LOYERM2_APPART,
            'nb_etablissements_culturels': sum([commune.etablissements_culturels.MUSEE_sum, commune.etablissements_culturels.OPERA_sum, commune.etablissements_culturels.C_CREATION_MUSI_sum, commune.etablissements_culturels.C_CREATION_ARTI_sum, commune.etablissements_culturels.C_CULTU_sum, commune.etablissements_culturels.SCENE_sum, commune.etablissements_culturels.THEATRE_sum, commune.etablissements_culturels.C_ART_sum, commune.etablissements_culturels.BIB_sum, commune.etablissements_culturels.CONSERVATOIRE_sum, commune.etablissements_culturels.CINEMA_sum]),
            'nb_etablissements_sportifs': sum([equipement.get_nombre() for equipement in commune.equipements_sportifs]),
            'interets_naturels': {
                'MER': commune.environnement_naturel.MER,
                'LAC': commune.environnement_naturel.LAC,
                'ESTUAIRE': commune.environnement_naturel.ESTUAIRE,
                'LOI_MONTAGNE': commune.environnement_naturel.LOI_MONTAGNE,
                'MASSIF': commune.environnement_naturel.MASSIF,
            },
            'nb_commerces': sum([commune.equipements_commerciaux.ALIMENTATION, commune.equipements_commerciaux.COMMERCES_GENERAUX, commune.equipements_commerciaux.LOISIRS, commune.equipements_commerciaux.BEAUTE_ET_ACCESSOIRES, commune.equipements_commerciaux.FLEURISTE_JARDINERIE_ANIMALERIE, commune.equipements_commerciaux.STATION_SERVICE])
        }

        return render_template("pages/resultats.html", infos_commune=infos_commune, index=session["index"]+1)

    except Exception as e:
        flash("Une erreur s'est produite lors de l'affichage des résultats de votre requête : "+ str(e))
        return render_template("erreurs/404.html")

        # Reste à faire : 
        # Marina en html : coder le bouton " voir le profil détaillé" qui assure la redirection vers cette route en transmettant la variable du code insee dans le template resultats.html
        # Pour Sarah/Anna après le code sur la route des utilisateurs : code ajout dans le panier, gérer le cas où il n'y a plus de résultats (peut-être à faire en amont ou en html)


############################################### ----- GILMAR ----- ###########################################################################################


# @app.route("/resultats/detail/<string:code_insee>") 
# def profil_detaille_commune(code_insee):
#     dico_codes_insee = dict() # creation dictionaire vide 'dico_codes_insee'
#     try:
#         form = ProfilDetailleCommune() # boutton ProfilDetailleCommune
#         if form.validate_on_submit(): # bouton cliqué
#             dico_codes_insee[code_insee] =  dico_codes_insee # stocke la variable recuperee 'code_insee' dans le dictionaire vide 'dico_codes_insee'
#             return redirect(url_for('profil_detaille_commune', code_insee=''))
#             flash("Bouton cliqué avec succès !")
    
    # except Exception as e:
    #     flash(f"ERREUR : {str(e)}. Le bouton n'a pas été encore cliqué !")
    
    # return render_template("pages/profil_detaille.html", form=form)


##########################################################################################################################################################


@app.route("/suivant/<int:index>")
@login_required
# coder en HTML/Jinja l'accès à cette route quand le bouton pour passer au résultat suivant est cliqué 
def page_suivante(index):
    # Passer à la page suivante
    session['index'] += 1
    return redirect(url_for('profil_commune', code_insee='', index=session['index']))
