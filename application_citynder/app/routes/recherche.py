from ..app import app
from flask import render_template, request, flash, redirect, url_for, session
import random
from sqlalchemy import or_, and_
from ..utils.calcul_loyer import calculer_loyer_m2_max, calculer_loyer_m2_min, normalisation_champs_texte
from ..models.formulaires import Recherche
from ..models.db_citynder import Commune, Environnement_naturel_specifique, Etablissements_culturels, Etablissements_commerciaux, Equipements_sportifs
from flask_login import login_required
import geopy.distance


@app.route("/recherche", methods=['GET', 'POST'])
@login_required
def recherche():
    """
    Route permettant une recherche filtrée dans la base de données. 
    Permet de stocker une liste de communes correspondant aux critères de recherche définis dans le formulaire dans une variable de session.

    Returns
    -------
    template
        Retourne le template profil_commune.html
    index
        Retoure index=0 : profil de la commune auyant 0 pour index dans la liste des communes retournée dans la variable de session.
    """
    query_results = Commune.query
    form = Recherche()

    try:
        if form.validate_on_submit() and form.validation(): # si le formulaire est bien rempli et validé

            # Loyer
            session['appart'] = request.form.get('appartement', None)
            session['maison'] = request.form.get('maison', None)
            session['appart_et_maison'] = request.form.get('appart_et_maison', None)

            session['loyer_min'] = request.form.get('loyer_min', None)
            session['loyer_max'] = request.form.get('loyer_max', None)
            session['surface_min'] = request.form.get('surface_min', None)
            session['surface_max'] = request.form.get('surface_max', None)


                # Calcul du loyer minimal et maximal à requêter d'après les informations remplies par l'utilisateur
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

            # Sports
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

            # Commerces 
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

            # Localisation
            session['coor'] = request.form.get('coor', None).strip("LatLng(").strip(")").split(',') 
            coords_centre_cercle = (session['coor'][0], session['coor'][1]) # coordonnées du centre du cercle sur la carte dans les filtres
            session['rayon'] = request.form.get('rayon', None) # rayon du cercle sur la carte dans les filtres
            rayon_km = float(session['rayon'])/1000 # conversion du rayon en km

            liste_codes_insee = [] 
            # itératon sur la liste de communes obtenue via les requêtes précédente réordonnée aléatoirement
            for result in random.sample(query_results.all(), k=len(query_results.all())) :  
                coords_result = (result.LATITUDE, result.LONGITUDE)
                distance = geopy.distance.geodesic(coords_centre_cercle, coords_result).km # on calcule la distance entre le centre du cercle de la carte et les coordonnées géographiques la ville
                if distance <= rayon_km : # si elle est inférieure au rayon, le point est dans le cercle
                    liste_codes_insee.append(result.INSEE_C)# ajout des codes insee des résultats dans une liste
                
                if len(liste_codes_insee)>=500 : # s'arrêter au 500e résultat
                    break

            if liste_codes_insee == []: # cas où il n'y aurait pas de résultat 
                flash("Aucun résultat ne correspond à tes attentes, tente à nouveau ta chance !", "warning")
                return redirect(url_for('recherche'))
            
            session['resultats'] = liste_codes_insee # stockage des résultats dans une variable de session

            return redirect(url_for('profil_commune', index=0))

    
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


@app.route("/resultats/<int:index>")
@login_required
def profil_commune(index):
    """
        Route permettant d'afficher le profil de la commune à partir de son index pour que l'utilisateur puisse l'ajouter à son panier ou l'ignorer.

        Parameters
        ----------
        index : int, required
            L'index de la commune dans la liste des résultats.

        Returns
        -------
        template
            Template d'affichage du résultat.
        id
            ID CSS du bloc résultat dans le template.
        infos_commune
            Dictionnaire contenant les informations de la commune à afficher
        index
            Index du premier résultat
    """
    try:
        
        # Récupérer la liste des codes INSEE des communes de la session
        liste_code_insee = session['resultats']

        if index>=len(liste_code_insee):
            
            flash("Il n'y a plus aucun résultat qui corresponde à tes critères, si tu en veux plus, élargis ta recherche", "info")
            return redirect(url_for('panier'))

         # Vérifier si l'index est validé, s'il n'est pas vide ou trop plein, supérieur à la liste totale des codes insee
        if index < 0 or index >= len(liste_code_insee):
            raise IndexError("Index n'est pas valide.")
        
        # Récupérer le code INSEE de la commune à partir de l'index
        code_insee = liste_code_insee[index]

        # Récupérer les informations de base de la commune à partir de la bdd
        commune = Commune.query.get(code_insee)
    
        # Vérifier si chaque attribut de l'établissement culturel existe et l'ajouter à la somme
        if getattr(commune, 'etablissements_culturels', None):
            nb_etablissements_culturels = sum([commune.etablissements_culturels.MUSEE_sum, commune.etablissements_culturels.OPERA_sum, commune.etablissements_culturels.C_CREATION_MUSI_sum, commune.etablissements_culturels.C_CREATION_ARTI_sum, commune.etablissements_culturels.C_CULTU_sum, commune.etablissements_culturels.SCENE_sum, commune.etablissements_culturels.THEATRE_sum, commune.etablissements_culturels.C_ART_sum, commune.etablissements_culturels.BIB_sum, commune.etablissements_culturels.CONSERVATOIRE_sum, commune.etablissements_culturels.CINEMA_sum]),
            nb_etablissements_culturels = nb_etablissements_culturels[0]
        else:
            nb_etablissements_culturels = 0 
        
        if getattr(commune, 'equipements_sportifs', None):
            nb_etablissements_sportifs = sum([equipement.get_nombre() for equipement in commune.equipements_sportifs]),
            nb_etablissements_sportifs = nb_etablissements_sportifs[0]
        else:
            nb_etablissements_sportifs = 0

        if getattr(commune, 'environnement_naturel', None):
            nb_environnement_naturels = {
                'MER': commune.environnement_naturel.MER,
                'LAC': commune.environnement_naturel.LAC,
                'ESTUAIRE': commune.environnement_naturel.ESTUAIRE,
                'LOI_MONTAGNE': commune.environnement_naturel.LOI_MONTAGNE,
                'MASSIF': commune.environnement_naturel.MASSIF,
            },
            nb_environnement_naturels = nb_environnement_naturels[0]
        else:
            nb_environnement_naturels = 0

        if getattr(commune, 'equipements_commerciaux', None):
            nb_commerces = sum([commune.equipements_commerciaux.ALIMENTATION, commune.equipements_commerciaux.COMMERCES_GENERAUX, commune.equipements_commerciaux.LOISIRS, commune.equipements_commerciaux.BEAUTE_ET_ACCESSOIRES, commune.equipements_commerciaux.FLEURISTE_JARDINERIE_ANIMALERIE, commune.equipements_commerciaux.STATION_SERVICE])
            nb_commerces = nb_commerces
        else:
            nb_commerces = 0

        id = f"bloc_resultat_{index%7}"
        print(id)
        # Stocker le résultat des requêtes dans un dictionnaire pour les transmettre au template
        infos_commune = { 
            'code_insee': code_insee,
            'nom_commune': commune.LIBGEO,
            'region': commune.REGION,
            'departement': commune.DEPARTEMENT,
            'prix_m2_maisons': commune.LOYERM2_MAISON,
            'prix_m2_appartements': commune.LOYERM2_APPART,
            'url_img' : commune.url_image,
            'prix_m2_maisons': round(commune.LOYERM2_MAISON,2),
            'prix_m2_appartements': round(commune.LOYERM2_APPART,2),
            'nb_etablissements_culturels': nb_etablissements_culturels,
            'nb_etablissements_sportifs': nb_etablissements_sportifs,
            'interets_naturels':nb_environnement_naturels,
            'nb_commerces': nb_commerces
        }
        
        return render_template("pages/resultats.html", infos_commune=infos_commune, index=index, id=id)

    except Exception as e:
        flash("Une erreur s'est produite lors de l'affichage des résultats de votre requête : "+ str(e))
        return render_template("erreurs/404.html")



@app.route("/resultats/detail/<string:code_insee>") 
@login_required
def profil_detaille_commune(code_insee):
    """
        Route permettant d'afficher le profil détaillé de la commune à partir de son code Insee.

        Parameters
        ----------
        code_insee : str, required
            Le code Insee de la commune à afficher.

        Returns
        -------
        template
            Template d'affichage du profil détaillé.
    """

    try:
        # Récupérer les informations de base de la commune à partir de la bdd
        commune = Commune.query.get(code_insee)

        # Vérifier si chaque attribut de l'établissement culturel existe et l'ajouter dans un dictionnaire ou une variable
        if getattr(commune, 'etablissements_culturels', None):
            culture = {
                'musee' : commune.etablissements_culturels.MUSEE_sum,
                'opera' : commune.etablissements_culturels.OPERA_sum,
                'crea_mus' : commune.etablissements_culturels.C_CREATION_MUSI_sum,
                'crea_art' : commune.etablissements_culturels.C_CREATION_ARTI_sum,
                'centre_culturel' : commune.etablissements_culturels.C_CULTU_sum,
                'scene' : commune.etablissements_culturels.SCENE_sum,
                'theatre': commune.etablissements_culturels.THEATRE_sum,
                'bibliotheque' : commune.etablissements_culturels.BIB_sum,
                'centre_artistique' : commune.etablissements_culturels.C_ART_sum,
                'conservatoire' :  commune.etablissements_culturels.CONSERVATOIRE_sum,
                'cinema' : commune.etablissements_culturels.CINEMA_sum,
            }
        else:
            culture = None 
        
        if getattr(commune, 'equipements_sportifs', None):
            etablissements_sportifs = sorted([(equipement.get_nombre(), equipement.nom_eq_sportif) for equipement in commune.equipements_sportifs], reverse=True)
        else:
            etablissements_sportifs = None

        if getattr(commune, 'environnement_naturel', None):
            interets_naturels = {
                'MER': commune.environnement_naturel.MER,
                'LAC': commune.environnement_naturel.LAC,
                'ESTUAIRE': commune.environnement_naturel.ESTUAIRE,
                'LOI_MONTAGNE': commune.environnement_naturel.LOI_MONTAGNE,
                'MASSIF': commune.environnement_naturel.MASSIF,
            },
        else:
            interets_naturels = None

        if getattr(commune, 'equipements_commerciaux', None):
            commerces = {
            'alimentation': commune.equipements_commerciaux.ALIMENTATION,
            'commerces_generaux': commune.equipements_commerciaux.COMMERCES_GENERAUX,
            'loisirs': commune.equipements_commerciaux.LOISIRS,
            'beaute_acessoires':commune.equipements_commerciaux.BEAUTE_ET_ACCESSOIRES,
            'fleur_jardin_animalerie': commune.equipements_commerciaux.FLEURISTE_JARDINERIE_ANIMALERIE,
            'station_service': commune.equipements_commerciaux.STATION_SERVICE,
            }
        else:
            commerces = None

        dico_code_insee = { 
            'code_insee': code_insee,
            'nom_commune': commune.LIBGEO,
            'population': commune.POP,
            'superficie': commune.SUPERFICIE,
            'region': commune.REGION,
            'departement': commune.DEPARTEMENT,
            'interets_naturels': interets_naturels,
            'etablissements_sportifs': etablissements_sportifs,
            'loyer_maison' : round(commune.LOYERM2_MAISON, 2),
            'loyer_appart' : round(commune.LOYERM2_APPART, 2),
            'url_img' : commune.url_image,
            'commerces': commerces,
            'culture' : culture
        }
                
        return render_template("pages/profil_detaille.html", dico_code_insee=dico_code_insee)

    except Exception as e: # en cas d'erreur
        flash(f"ERREUR : {str(e)}")
        return render_template("erreur/404.html")
