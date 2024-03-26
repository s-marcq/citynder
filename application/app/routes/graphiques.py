from ..app import app, db
from flask import render_template, request, flash, jsonify
from flask_login import login_required
from ..models.db_citynder import Commune, Etablissements_culturels
from sqlalchemy.sql import func

# définition de la route pour afficher le graphique
@app.route("/graphiques/moyenne_loyer_par_region", methods=['GET', 'POST']) 
def graphique_loyer_par_region(): 
    # renvoie le template HTML pour afficher le graphique
    return render_template("pages/graphiques/moyenne_loyer_par_region.html") 

# définition de la route pour fournir les données du graphique via une requête
@app.route('/moyenne_loyer_par_region_data', methods=['GET', 'POST']) 
def moyenne_loyer_par_region_data():  
    # récupère les régions et leur moyenne de loyer par mètre carré à partir de la base de données
    regions = Commune.query.with_entities(Commune.REGION, func.avg((Commune.LOYERM2_APPART + Commune.LOYERM2_MAISON)/2)).group_by(Commune.REGION).all()
    
    # initialise une liste vide pour stocker les données à renvoyer
    data = []
    # parcours des régions et de leur moyenne de loyer
    for region in regions:
        # ajoute les données de chaque région à la liste
        data.append({
            'label': region[0], # le nom de la région
            'nombre': round(region[1], 2), # la moyenne de loyer arrondie à deux décimales
        })
    
    # renvoie les données au format JSON
    return jsonify(data)
