from ..app import app, db
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models.db_citynder import Utilisateurs, Commune
from sqlalchemy.sql import text
# from ..models.formulaires import  

@app.route("/panier", methods=['GET', 'POST']) 
@app.route("/panier/<int:page>", methods=['GET', 'POST']) 
@login_required
def panier() :

    try:
        # code affichage du panier
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
                print(favori)
                communes.append(dico)
                communes = sorted(communes, key=lambda x: x['favori'], reverse=True)

        # gérer la pagination

        # code mettre un élément en favori
                
    
    except Exception as e :
        flash("L'affichage du panier a rencontré une erreur : "+ str(e))
    return render_template("pages/panier.html", communes=communes, id=id)

@app.route("/panier/suppression/<string:code_insee>", methods=['GET', 'POST']) 
@login_required
def suppression_panier(code_insee) :
    try : 
        id = current_user.USER_ID
        if current_user.is_authenticated :
            sql = f'DELETE FROM Contenu_panier_utilisateurs WHERE INSEE_C_item={code_insee} AND USER_ID={id}'
            db.session.execute(text(sql))
            db.session.commit()
            flash("Suppression réalisée avec succès", "success")

    except Exception as e :
        flash("La suppression a rencontré une erreur : "+ str(e))
    return redirect(url_for('panier'))

@app.route("/panier/modif_favori/<string:code_insee>/<string:favori>", methods=['GET', 'POST']) 
@login_required
def modif_favori(code_insee, favori) :
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


