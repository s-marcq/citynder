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


@app.route("/recherche", methods=['GET', 'POST'])
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

            loyer_m2_min = calculer_loyer_m2_min(session['loyer_min'], session['surface_min'], session['surface_max'])
            loyer_m2_max = calculer_loyer_m2_max(session['loyer_max'], session['surface_min'], session['surface_max'])

            # régler le cas où c'est mal rempli

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
                Commune.query.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Terrain de football")

            session['piscine'] = request.form.get("piscine", None)
            if session['piscine']:
                Commune.query.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Piscine/Bassin exercice aquatique")

            session['rando'] = request.form.get("rando", None)
            if session['rando']:
                Commune.query.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Boucle de randonnée")

            session['sportco'] = request.form.get("sportco", None)
            if session['sportco']:
                Commune.query.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Salles de pratiques collectives / gymnase")

            session['escalade'] = request.form.get("escalade", None)
            if session['escalade']:
                Commune.query.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Equipement escalade")


            session['petanque'] = request.form.get("petanque", None)
            if session['petanque']:
                Commune.query.join(Commune.equipements_sportifs).filter(Equipements_sportifs.nom_eq_sportif == "Terrain de pétanque")

            # commerces 
            session['com_alim'] = request.form.get("com_alim", None)
                #query_results = query_results.join(Commune.equipements_commerciaux).filter(Etablissements_commerciaux.ALIMENTATION > 0)
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
                    print('ok zero')
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
            match session['pop']:
                case '':
                    Commune.query.filter(Commune.POP == ...)

            # Département
            if session['département'] :
                Commune.query.filter(Commune.DEPARTEMENT == ...)
            
                  # Département
            if session['région'] :
                Commune.query.filter(Commune.REGION == ...)



            # Mettre les codes insee des résultats dans une liste, les mélanger et les mettre dans une variable de session
            liste_codes_insee = [resultat.INSEE_C for resultat in query_results] 
            # cas où il n'y aurait pas de résultat  
            if liste_codes_insee == []:
                flash("Aucun résultat, veuillez réessayer")
                return redirect(url_for('recherche'))
            liste_codes_insee = random.sample(liste_codes_insee, k=len(liste_codes_insee))
            session['resultats'] = liste_codes_insee
            session['index']= 0  

            for resultat in liste_codes_insee :
                resultat = Commune.query.filter(Commune.INSEE_C == resultat).first()
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

@app.route("/resultats/detail/<string:code_insee>") 
def profil_detaille_commune(code_insee):
    dico_codes_insee = dict() # creation dictionaire vide 'dico_codes_insee'
    try:
        form = ProfilDetailleCommune() # boutton ProfilDetailleCommune
        if form.validate_on_submit(): # bouton cliqué
            dico_codes_insee[code_insee] =  dico_codes_insee # stocke la variable recuperee 'code_insee' dans le dictionaire vide 'dico_codes_insee'
            return redirect(url_for('profil_detaille_commune', code_insee=''))
            flash("Bouton cliqué avec succès !")
    
    except Exception as e:
        flash(f"ERREUR : {str(e)}. Le bouton n'a pas été encore cliqué !")
    
    return render_template("pages/profil_detaille.html", form=form)

@app.route("/suivant/<int:index>")
# coder en HTML/Jinja l'accès à cette route quand le bouton pour passer au résultat suivant est cliqué 
def page_suivante(index):
    # Passer à la page suivante
    session['index'] += 1
    return redirect(url_for('profil_commune', code_insee='', index=session['index']))

@app.route("/")
def route_test_bdd():
    test = Commune.query.join(Commune.equipements_commerciaux).filter((Etablissements_commerciaux.LOISIRS+Etablissements_commerciaux.STATION_SERVICE) ==17).first()
    print(f"Commune : {test}\n, Interet naturel : {test.environnement_naturel} \n culture : {test.etablissements_culturels} \n commerce : {test.equipements_commerciaux} \n sport : {test.equipements_sportifs}")
    return "ok"

