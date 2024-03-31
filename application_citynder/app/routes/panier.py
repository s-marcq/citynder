from ..app import app, db
from flask import render_template, flash, redirect, url_for, session
from flask_login import current_user, login_required
from ..models.db_citynder import Utilisateurs, Commune
from sqlalchemy.sql import text

@app.route("/panier", methods=['GET', 'POST']) 
@login_required
def panier() :
    """
    Route permettant l'affichage du panier de l'utilisateur.

    Returns
    -------
    template
        Retourne le template panier.html avec l'ID de l'utilisateur et les communes présentes dans son panier.
    """
    try:
        id = current_user.USER_ID
        if current_user.is_authenticated :
            communes = []
            communes_panier = Commune.query.join(Utilisateurs.panier).filter(Utilisateurs.USER_ID==id)
            for commune in communes_panier :
                # Cas des communes avec arrondissements (posent problème dans les url du boncoin)
                if 'Paris ' in commune.LIBGEO :
                    url_leboncoin = "https://www.leboncoin.fr/recherche?category=10&locations="+"Paris"
                elif 'Marseille ' in commune.LIBGEO :
                    url_leboncoin = "https://www.leboncoin.fr/recherche?category=10&locations="+"Marseille"
                elif 'Lyon ' in commune.LIBGEO :
                    url_leboncoin = "https://www.leboncoin.fr/recherche?category=10&locations="+"Lyon"
                # Casa des communes sans arrondissements
                else : 
                    url_leboncoin = "https://www.leboncoin.fr/recherche?category=10&locations="+commune.LIBGEO
                
                sql_favori = f'SELECT FAVORI FROM Contenu_panier_utilisateurs WHERE INSEE_C_item={commune.INSEE_C} AND USER_ID={id} LIMIT 1'
                favori = db.session.execute(text(sql_favori)).first()

                dico = {"LIBGEO": commune.LIBGEO,
                                 "INSEE_C" : commune.INSEE_C,
                                 "DEPARTEMENT": commune.DEPARTEMENT,
                                 "url_image": commune.url_image,
                                 "url_se_loger" : "https://www.seloger.com/list.htm?tri=initial&enterprise=0&idtypebien=2,1&idtt=1&naturebien=1&ci="+commune.INSEE_C[:2]+"0"+commune.INSEE_C[2:]+"&m=search_hp_new",
                                 "url_leboncoin" : url_leboncoin,
                                 "favori" : str(favori[0]) }
                communes.append(dico)
                communes = sorted(communes, key=lambda x: x['favori'], reverse=True)

    
    except Exception as e :
        flash("L'affichage du panier a rencontré une erreur : "+ str(e))
    return render_template("pages/panier.html", communes=communes, id=id)

@app.route("/panier/suppression/<string:code_insee>", methods=['GET', 'POST']) 
@login_required
def suppression_panier(code_insee) :
    """
    Route permettant à l'utilisateur de supprimer une commune de son panier.

    Parameters
    ----------
    code_insee : str, required
        Le code INSEE de la commune à supprimer du panier.

    Returns
    -------
    redirection
        Redirige vers la route 'panier'.
    """

    try : 
        id = current_user.USER_ID
        if current_user.is_authenticated :
            sql = f'DELETE FROM Contenu_panier_utilisateurs WHERE INSEE_C_item={code_insee} AND USER_ID={id}'
            db.session.execute(text(sql))
            db.session.commit()
            flash("Ajout réalisée avec succès", "success")

    except Exception as e :
        flash("La suppression a rencontré une erreur : "+ str(e))
    return redirect(url_for('panier'))

@app.route("/panier/modif_favori/<string:code_insee>/<string:favori>", methods=['GET', 'POST']) 
@login_required
def modif_favori(code_insee, favori) :
    """
    Route permettant à l'utilisateur d'enregistrer une commune dans sa liste des favoris ou de la retirer de cette liste.

    Parameters
    ----------
    code_insee : str, required
        Le code INSEE de la commune à ajouter ou retirer de la liste des favoris.

    favori : str, required
        Indique si la commune est enregistré en tant que favorite ou non (booléen 0 ou 1).

    Returns
    -------
    redirection
        Redirige vers la route 'panier'.
    """
    try : 
        id = current_user.USER_ID
        if current_user.is_authenticated :
            if favori == "0":
                favori = '1'
            else : 
                favori='0'

            sql = f'UPDATE Contenu_panier_utilisateurs SET FAVORI={favori} WHERE INSEE_C_item={code_insee} AND USER_ID={id}'
            db.session.execute(text(sql))
            db.session.commit()

    except Exception as e :
        flash("La modification a rencontré une erreur : "+ str(e))
    return redirect(url_for('panier'))


@app.route("/panier/ajout/<int:index>", methods=['GET', 'POST']) 
@login_required
def ajout_panier(index) :
    """
    Route permettant à l'utilisateur d'ajouter une commune dans son panier.

    Parameters
    ----------
    index : int, required
        L'index de la commune à ajouter dans la liste des résultats.

    Returns
    -------
    redirection
        Redirige vers la route 'profil_commune' pour aller au résultat suivant.
    """

    try : 
        liste_code_insee = session['resultats']
        code_insee = liste_code_insee[index]

        id = current_user.USER_ID
        if current_user.is_authenticated :
            sql = f'INSERT INTO Contenu_panier_utilisateurs (INSEE_C_item, USER_ID, FAVORI) VALUES ({code_insee}, {id}, false)'
            db.session.execute(text(sql))
            db.session.commit()
            flash("Ajout réalisé avec succès", "success")

    except Exception as e :
        flash("L'ajout a rencontré une erreur : "+ str(e))
    return redirect(url_for('profil_commune', index=index+1))
