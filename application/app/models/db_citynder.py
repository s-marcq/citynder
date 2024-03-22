from ..app import db #, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_method

# tables de jointure :  equipements sportifs et paniers utilisateurs (relations many-to-many)
commune_equipements_sportifs = db.Table(
    "Commune_Equipements_sportifs",
    db.Column("INSEE_C", db.Integer, db.ForeignKey('Commune.INSEE_C'), nullable=False, primary_key=True),
    # /!\ Inversion nombre et sport_id --> le nombre correspond au sport_id
    db.Column("nombre", db.Integer, db.ForeignKey('Equipements_sportifs.sport_id'), nullable=False),
    db.Column("sport_id", db.Integer) # le sport_id correspond au nombre
    )

contenu_paniers_utilisateurs = db.Table(
    "Contenu_panier_utilisateurs",
    db.Column("INSEE_C_item", db.String(5), db.ForeignKey('Commune.INSEE_C'), nullable=False),
    db.Column("USER_ID", db.Integer, db.ForeignKey('Utilisateurs.USER_ID'), nullable=False),
    db.Column("FAVORI", db.Boolean, nullable=False),
    db.Column("ID_item", db.Integer, primary_key=True, autoincrement=True, nullable=False)
    )

# classes : relations one-to-many
class Commune(db.Model):
    __tablename__ = "Commune"
    INSEE_C = db.Column(db.String(5), primary_key=True, unique=True, nullable=False)
    ID_ZONE = db.Column(db.Integer)
    LIBGEO = db.Column(db.String(50), nullable=False)
    DEPARTEMENT = db.Column(db.String(45), nullable=False)
    REGION = db.Column(db.Integer, nullable=False)
    LOYERM2_MAISON = db.Column(db.Float, nullable=False)
    TYPPRED_MAISON = db.Column(db.Text, nullable=False)
    PRECISION_MAISON = db.Column(db.String(50))
    LOYERM2_APPART = db.Column(db.Float, nullable=False)
    TYPPRED_APPART = db.Column(db.Text, nullable=False)
    PRECISION_APPART = db.Column(db.String(50))
    POP = db.Column(db.Integer)
    SUPERFICIE = db.Column(db.Float)
    LATITUDE = db.Column(db.Float)
    LONGITUDE = db.Column(db.Float)
    INTERET_NATUREL = db.Column(db.Boolean)
    NBRE_HEBERGEMENTS_TOURISTIQUES = db.Column(db.Integer)
    url_image = db.Column(db.Text)

    # propriétés de relation
    environnement_naturel = db.relationship("Environnement_naturel_specifique", backref="environnement_naturel", uselist=False)
    etablissements_culturels = db.relationship("Etablissements_culturels", backref="etablissements_culturels", uselist=False)
    equipements_commerciaux = db.relationship("Etablissements_commerciaux", backref="etablissements_commerciaux",uselist=False)

    # relation vers la table de relation entre la commune et les équipements sportifs
    equipements_sportifs = db.relationship(
        'Equipements_sportifs', 
        secondary=commune_equipements_sportifs, 
        backref="equipements_sportifs"
    )


    def __repr__(self):
        return f"<Commune {dict(INSEE_C=self.INSEE_C, ID_ZONE=self.ID_ZONE, LIBGEO=self.LIBGEO, DEPARTEMENT=self.DEPARTEMENT, REGION=self.REGION, LOYERM2_MAISON=self.LOYERM2_MAISON, TYPPRED_MAISON=self.TYPPRED_MAISON, PRECISION_MAISON=self.PRECISION_MAISON, LOYERM2_APPART=self.LOYERM2_APPART, TYPPRED_APPART=self.TYPPRED_APPART, PRECISION_APPART=self.PRECISION_APPART, POP=self.POP, SUPERFICIE=self.SUPERFICIE, LATITUDE=self.LATITUDE, LONGITUDE=self.LONGITUDE, INTERET_NATUREL=self.INTERET_NATUREL, NBRE_HEBERGEMENTS_TOURISTIQUES=self.NBRE_HEBERGEMENTS_TOURISTIQUES)}>"


class Environnement_naturel_specifique(db.Model):
    __tablename__ = "Environnement_naturel_specifique"
    MER = db.Column(db.Boolean)
    LAC = db.Column(db.Boolean)
    ESTUAIRE = db.Column(db.Boolean)
    LOI_MONTAGNE = db.Column(db.Boolean)
    MASSIF = db.Column(db.String(50))
    PN_LIBGEO = db.Column(db.String(50))
    PNR_LIBGEO = db.Column(db.String(50))

    # clé étrangère
    INSEE_C = db.Column(
        db.String(5),  
        db.ForeignKey('Commune.INSEE_C'), 
        primary_key=True
    )

    def __repr__(self):
        return f"<Environnement_naturel_specifique {dict(MER=self.MER, LAC=self.LAC, ESTUAIRE=self.ESTUAIRE, LOI_MONTAGNE=self.LOI_MONTAGNE, MASSIF=self.MASSIF, PN_LIBGEO=self.PN_LIBGEO, PNR_LIBGEO=self.PNR_LIBGEO, INSEE_C=self.INSEE_C)}>"

class Etablissements_culturels(db.Model):
    __tablename__ = "Etablissements_culturels"
    MUSEE_sum = db.Column(db.Integer)
    OPERA_sum = db.Column(db.Integer)
    C_CREATION_MUSI_sum = db.Column(db.Integer)
    C_CREATION_ARTI_sum = db.Column(db.Integer)
    C_CULTU_sum = db.Column(db.Integer)
    SCENE_sum = db.Column(db.Integer)
    THEATRE_sum = db.Column(db.Integer)
    C_ART_sum = db.Column(db.Integer)
    BIB_sum = db.Column(db.Integer)
    CONSERVATOIRE_sum = db.Column(db.Integer)
    CINEMA_sum = db.Column(db.Integer)


    # clé étrangère
    INSEE_C = db.Column(
        db.String(5),  
        db.ForeignKey('Commune.INSEE_C'),
        primary_key=True
    )


    def __repr__(self):
        return f"<Etablissements_culturels {dict(MUSEE_sum=self.MUSEE_sum, OPERA_sum=self.OPERA_sum, C_CREATION_MUSI_sum=self.C_CREATION_MUSI_sum, C_CREATION_ARTI_sum=self.C_CREATION_ARTI_sum, C_CULTU_sum=self.C_CULTU_sum, SCENE_sum=self.SCENE_sum, THEATRE_sum=self.THEATRE_sum, C_ART_sum=self.C_ART_sum, BIB_sum=self.BIB_sum, CONSERVATOIRE_sum=self.CONSERVATOIRE_sum, CINEMA_sum=self.CINEMA_sum, INSEE_C=self.INSEE_C)}>"

class Etablissements_commerciaux(db.Model):
    __tablename__ = "Etablissements_commerciaux"
    ALIMENTATION = db.Column(db.Integer)
    COMMERCES_GENERAUX = db.Column(db.Integer)
    LOISIRS = db.Column(db.Integer)
    BEAUTE_ET_ACCESSOIRES = db.Column(db.Integer)
    FLEURISTE_JARDINERIE_ANIMALERIE = db.Column(db.Integer)
    STATION_SERVICE = db.Column(db.Integer)

    # clé étrangère
    INSEE_C = db.Column(
        db.String(5),  
        db.ForeignKey('Commune.INSEE_C'),
        primary_key=True
    )

    def __repr__(self):
        return f"<Etablissements_commerciaux {dict(ALIMENTATION=self.ALIMENTATION, COMMERCES_GENERAUX=self.COMMERCES_GENERAUX, LOISIRS=self.LOISIRS, BEAUTE_ET_ACCESSOIRES=self.BEAUTE_ET_ACCESSOIRES, FLEURISTE_JARDINERIE_ANIMALERIE=self.FLEURISTE_JARDINERIE_ANIMALERIE, STATION_SERVICE=self.STATION_SERVICE, INSEE_C=self.INSEE_C)}>"

class Equipements_sportifs(db.Model):
    __tablename__ = "Equipements_sportifs"
    sport_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    nom_eq_sportif = db.Column(db.Text, nullable=False)
    
    # méthode permettant d'
    
    def get_nombre(self):
        """
            Permet d'aller chercher le nombre du type d'équipement sportif en question au sein de la commune dans la base (table commune_equipements_sportifs)

            Returns
            -------
            integer
                La quantité de cet équipement dans la commune.
        """
        nombre = db.session.query(commune_equipements_sportifs.c.sport_id).filter_by(nombre=self.sport_id).first()
        return nombre[0]
    
    def __repr__(self):
        return f"<Equipements_sportifs {dict(sport_id=self.sport_id, nom_eq_sportif=self.nom_eq_sportif, nombre=self.get_nombre())}>"

class Utilisateurs(UserMixin, db.Model):
    __tablename__ = "Utilisateurs"
    USER_ID = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    EMAIL = db.Column(db.String(50))
    MDP = db.Column(db.String(20))

    # relation vers la table le contenu du panier -> renvoie des utilisateurs, revoir
    panier = db.relationship('Commune', secondary = contenu_paniers_utilisateurs, backref="communes_selectionnees")

    def __repr__(self):
        return f"<Utilisateurs {dict(USER_ID=self.USER_ID, EMAIL=self.EMAIL, MDP=self.MDP)}>"

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

    # def get_id(self):
    #     return self.USER_ID

    # @login.user_loader
    # def get_user_by_id(USER_ID):
    #     return Utilisateurs.query.get(int(USER_ID))