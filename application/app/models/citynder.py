from ..app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# tables de jointure :  equipements sportifs et paniers utilisateurs (relations many-to-many)
commune_equimements_sportifs = db.Table(
    "Commune_Equimements_sportifs",
    db.Column("Commune", db.Integer, db.ForeignKey('Commune.INSEE_C'), nullable=False),
    db.Column("Equipements_sportifs", db.Integer, db.ForeignKey('Equipements_sportifs.sport_id'), nullable=False)
    )

contenu_paniers_utilisateurs = db.Table(
    "Contenu_paniers_utilisateurs",
    db.Column("INSEE_C", db.Integer, db.ForeignKey('Commune.INSEE_C'), nullable=False),
    db.Column("USER_ID", db.Integer, db.ForeignKey('Utilisateurs.USER_ID'), nullable=False),
    db.Column("FAVORI", db.Boolean)
    )

# classes : relations one-to-many

class Commune(db.Model):
    __tablename__ = "Commune"
    INSEE_C = db.Column(db.String(6), primary_key=True, unique=True, nullable=False)
    ID_ZONE = db.Column(db.String(45))
    LIBGEO = db.Column(db.String(45), nullable=False)
    DEPARTEMENT = db.Column(db.String(45), nullable=False)
    REGION = db.Column(db.Integer, nullable=False)
    LOYERM2_MAISON = db.Column(db.Float, nullable=False)
    TYPRED_MAISON = db.Column(db.String(10), nullable=False)
    PRECISION_MAISON = db.Column(db.String(45))
    LOYERM2_APPART = db.Column(db.Float, nullable=False)
    TYPRED_APPART = db.Column(db.String(10), nullable=False)
    PRECISION_APPART = db.Column(db.String(45))
    POP = db.Column(db.Integer)
    LATITUDE = db.Column(db.Numeric)
    LONGITUDE = db.Column(db.Numeric)
    INTERET_NATUREL = db.Column(db.Boolean)
    NBRE_HEBERGEMENTS_TOURISTIQUES = db.Column(db.Integer)

    # propriétés de relation
    environnement_naturel = db.relationship("Environnement_naturel_specifique", backref="environnement_naturel")
    etablissements_culturels = db.relationship("Etablissements_culturels", backref="etablissements_culturels")
    equipements_commerciaux = db.relationship("Equipements_commerciaux", backref="equipements_commerciaux")

    # relation vers la table de relation entre la commune et les équipements sportifs
    equipements_sportifs = db.relationship(
        'Equipements_sportifs', 
        secondary=commune_equimements_sportifs, 
        backref="equipements_sportifs"
    )

class Environnement_naturel_specifique(db.Model):
    __tablename__ = "Environnement_naturel_specifique"
    MER = db.Column(db.Boolean)
    LAC = db.Column(db.Boolean)
    ESTUAIRE = db.Column(db.Boolean)
    LOI_MONTAGNE = db.Column(db.Boolean)
    MASSIF = db.Column(db.String(45))
    PN_LIBGEO = db.Column(db.String(45))
    PNR_LIBGEO = db.Column(db.String(45))

    # clé étrangère
    INSEE_C = db.Column(
        db.String(6),  
        db.ForeignKey('Commune.INSEE_C')
    )

class Etablissements_culturels(db.Model):
    __tablename__ = "Etablissements_culturels"
    MUSEE = db.Column(db.Integer)
    OPERA = db.Column(db.Integer)
    C_CREATION_MUSI = db.Column(db.Integer)
    C_CREATION_ARTI = db.Column(db.Integer)
    C_CULTU = db.Column(db.Integer)
    SCENE = db.Column(db.Integer)
    THEATRE = db.Column(db.Integer)
    C_ART = db.Column(db.Integer)
    BIB = db.Column(db.Integer)
    CONSERVATOIRE = db.Column(db.Integer)
    CINEMA = db.Column(db.Integer)


    # clé étrangère
    INSEE_C = db.Column(
        db.String(6),  
        db.ForeignKey('Commune.INSEE_C')
    )

class Equipements_commerciaux(db.Model):
    __tablename__ = "Equipements_commerciaux"
    ALIMENTATION = db.Column(db.Integer)
    COMMERCES_GENERAUX = db.Column(db.Integer)
    LOISIRS = db.Column(db.Integer)
    BEAUTE_ET_ACCESSOIRES = db.Column(db.Integer)
    FLEURISTE_JARDINERIE_ANIMALERIE = db.Column(db.Integer)
    STATION_SERVICE = db.Column(db.Integer)

    # clé étrangère
    INSEE_C = db.Column(
        db.String(6),  
        db.ForeignKey('Commune.INSEE_C')
    )

class Equipements_sportifs(db.Model):
    __tablename__ = "Equipements_sportifs"
    sport_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    nom_eq_sportif = db.Column(db.String(45), nullable=False)

class Utilisateurs(UserMixin, db.Model):
    __tablename__ = "Utilisateurs"
    USER_ID = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    EMAIL = db.Column(db.String(80))
    MDP = db.Column(db.String(100))

    # relation vers la table de relation du contenu du panier
    panier = db.relationship(
        'Contenu_paniers_utilisateurs', 
        secondary=contenu_paniers_utilisateurs, 
        backref="communes_selectionnees"
    )

    # méthodes pour la gestion des utilisateurs
    @staticmethod
    def identification(EMAIL, MDP):
        utilisateur = Utilisateurs.query.filter(Utilisateurs.EMAIL == EMAIL).first()
        if utilisateur and check_password_hash(utilisateur.MDP, MDP):
            return utilisateur
        return None

    @staticmethod
    def ajout(EMAIL, MDP):
        erreurs = []
        if not MDP or len(MDP) < 6:
            erreurs.append("Le mot de passe est vide ou trop court")
        if not EMAIL :
            erreurs.append("Le mail est vide")

        unique = Utilisateurs.query.filter(
            db.or_(Utilisateurs.EMAIL == EMAIL)
        ).count()
        if unique > 0:
            erreurs.append("L'utilisateur existe déjà avec le mail "+EMAIL)

        if len(erreurs) > 0:
            return False, erreurs
        
        utilisateur = Utilisateurs(
            MDP=generate_password_hash(MDP),
            EMAIL=EMAIL
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            db.session.rollback()
            return False, [str(erreur)]

    def get_id(self):
        return self.USER_ID

    @login.user_loader
    def get_user_by_id(USER_ID):
        return Utilisateurs.query.get(int(USER_ID))