from ..app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
    """
    Une classe représentant la commune.

    Attributes
    ----------
    INSEE_C : sqlalchemy.sql.schema.Column
        Code Insee de la commune. C'est la clé primaire. Cet attribut est une Column SQLALchemy.
    ID_ZONE : sqlalchemy.sql.schema.Column
        Identifiant de la zone géographique dans laquelle se trouve la commune.
    LIBGEO : sqlalchemy.sql.schema.Column
        Libellé géographique
    DEPARTEMENT : sqlalchemy.sql.schema.Column
        Département
    REGION : sqlalchemy.sql.schema.Column
        Région
    LOYERM2_MAISON : sqlalchemy.sql.schema.Column
        indicateur du prix du mètre carré pour les maisons
    TYPPRED_MAISON : sqlalchemy.sql.schema.Column
        type de prédiction du loyer pour les maisons
    PRECISION_MAISON : sqlalchemy.sql.schema.Column
        colonne précisant un éventuel manque de précision dans l'indicateur des loyers pour les maisons
    LOYERM2_APPART : sqlalchemy.sql.schema.Column
        indicateur du prix du mètre carré pour les appartements
    TYPPRED_APPART : sqlalchemy.sql.schema.Column
        type de prédiction du loyer pour les appartements
    PRECISION_APPART : sqlalchemy.sql.schema.Column
        colonne précisant un éventuel manque de précision dans l'indicateur des loyers appartements
    POP : sqlalchemy.sql.schema.Column
        population de la commune
    SUPERFICIE : sqlalchemy.sql.schema.Column
        superficie de la commune
    LATITUDE : sqlalchemy.sql.schema.Column
        latitude
    LONGITUDE : sqlalchemy.sql.schema.Column
        longitude
    INTERET_NATUREL : sqlalchemy.sql.schema.Column
        booléen : commune d'interêt naturel 
    NBRE_HEBERGEMENTS_TOURISTIQUES : sqlalchemy.sql.schema.Column
        nombre d'hébergements touristiques
    url_image : sqlalchemy.sql.schema.Column
        url de l'image de la ville sur wikidata
    environnement_naturel : sqlalchemy.orm.relationship
        Attribut de relation avec l'environnement naturel
    etablissements_culturels : sqlalchemy.orm.relationship
        Attribut de relation avec les établissements culturels
    equipements_commerciaux : sqlalchemy.orm.relationship
        Attribut de relation avec les équipemets commerciaux
    equipements_sportifs : sqlalchemy.orm.relationship
        Attribut de relation avec les équipements sportifs

    """
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
    """
    Une classe représentant l'environnement naturel de la commune.

    Attributes
    ----------
    MER : sqlalchemy.sql.schema.Column
        Commune concernée ou non par la Loi littoral par la présence de la mer. Cet attribut est une Column SQLALchemy.
    LAC : sqlalchemy.sql.schema.Column
        Commune concernée ou non par la Loi littoral par la présence d'un lac.
    ESTUAIRE : sqlalchemy.sql.schema.Column
        Commune concernée ou non par la Loi littoral par la présence d'un estuaire.
    LOI_MONTAGNE : sqlalchemy.sql.schema.Column
        Commune concernée ou non par la Loi montagne.
    MASSIF : sqlalchemy.sql.schema.Column
        Nom du massif dans lequel se trouve la commune.
    PN_LIBGEO : sqlalchemy.sql.schema.Column
        Nom du parc naturel dans lequel se trouve la commune.
    PNR_LIBGEO : sqlalchemy.sql.schema.Column
        Nom du parc naturel régional dans lequel se trouve la commune.
    INSEE_C : sqlalchemy.sql.schema.Column
        Code Insee de la commune. C'est la clé étragère. 
    """
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
    """
    Une classe représenant les établissements culturels des communes.

    Attributes
    ----------
    MUSEE_sum  : sqlalchemy.sql.schema.Column
        Nombre de musées
    OPERA_sum  : sqlalchemy.sql.schema.Column
        Nombre d'opéras
    C_CREATION_MUSI_sum  : sqlalchemy.sql.schema.Column
        Nombre de centres de création musicale
    C_CREATION_ARTI_sum  : sqlalchemy.sql.schema.Column
        Nombre de centres de création artistique
    C_CULTU_sum  : sqlalchemy.sql.schema.Column
        Nombre de centres culturels
    SCENE_sum  : sqlalchemy.sql.schema.Column
        Nombre de scènes
    THEATRE_sum  : sqlalchemy.sql.schema.Column
        Nombre de théâtres
    C_ART_sum  : sqlalchemy.sql.schema.Column
        ???
    BIB_sum  : sqlalchemy.sql.schema.Column
        Nombre de bibliothèques
    CONSERVATOIRE_sum  : sqlalchemy.sql.schema.Column
        Nombre de conservatoires
    CINEMA_sum  : sqlalchemy.sql.schema.Column
        Nombre de cinémas
    INSEE_C : sqlalchemy.sql.schema.Column
        Code Insee de la commune. C'est la clé étragère. 
    """
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
    """
    Une classe représentant les établissements commerciaux d'une commune.

    Attributes
    ----------
    ALIMENTATION  : sqlalchemy.sql.schema.Column
        Nombre de commerces d'alimentation
    COMMERCES_GENERAUX  : sqlalchemy.sql.schema.Column
        Nombre de commerces généraux
    LOISIRS  : sqlalchemy.sql.schema.Column
        Nombre de commerces de loisir
    BEAUTE_ET_ACCESSOIRES  : sqlalchemy.sql.schema.Column
        Nombre de commerces de beauté et accessoires
    FLEURISTE_JARDINERIE_ANIMALERIE  : sqlalchemy.sql.schema.Column
        Nombre de fleuristes/jardineries/animaleries
    STATION_SERVICE  : sqlalchemy.sql.schema.Column
        Nombre de stations-service
    INSEE_C : sqlalchemy.sql.schema.Column
        Code Insee de la commune. C'est la clé étragère. 
    """
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
    """
    Une classe représentant les types d'équipements sportifs.

    Attributes
    ----------
    sport_id  : sqlalchemy.sql.schema.Column
        Clé unique non nulle servant d'identifiant de l'équipement
    nom_eq_sportif  : sqlalchemy.sql.schema.Column
        Nom de l'équipemeny sportif
    """
    __tablename__ = "Equipements_sportifs"
    sport_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    nom_eq_sportif = db.Column(db.Text, nullable=False)
        
    def get_nombre(self):
        """
            Permet d'aller chercher le nombre du type d'équipement sportif en question au sein de la commune dans la base (stocké table commune_equipements_sportifs)

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
    """
    Une classe représentant les utilisateurs de l'application.

    Attributes
    ----------
    USER_ID : sqlalchemy.sql.schema.Column
        Identifiant de l'utilisateur. C'est la clé primaire. Cet attribut est une Column SQLALchemy.
    EMAIL : sqlalchemy.sql.schema.Column
        Adresse mail de l'utilisateur.
    MDP : sqlalchemy.sql.schema.Column
        Mot de passé hashé de l'utilisateur.

    Methods
    -------
    identification(mail, password)
        Permet l'identification d'un utilisateur à partir d'un  mail et d'un mot de passe fournis.
    ajout(mail, password)
        Permet l'ajout d'un utilisateur à partir d'un  mail et d'un mot de passe fournis.
    """
    __tablename__ = "Utilisateurs"
    USER_ID = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    EMAIL = db.Column(db.String(50))
    MDP = db.Column(db.String(20))

    # relation vers la table le contenu du panier -> renvoie des utilisateurs, revoir
    panier = db.relationship('Commune', secondary = contenu_paniers_utilisateurs, backref="communes_selectionnees")

    # méthodes pour la gestion des utilisateurs
    @staticmethod
    def identification(EMAIL, MDP):
        """
        Permet l'identification d'un utilisateur à partir d'un  mail et d'un mot de passe fournis

        Les deux arguments sont obligatoires

        Parameters
        ----------
        mail : str, required
            Le mail fourni par le client
        password : str, required
            Le mot de passe fourni par le client

        Returns
        -------
        app.models.users.Users
            Une instance de la classe Users si l'identification est un succès, sinon retourne None
        """
        utilisateur = Utilisateurs.query.filter(Utilisateurs.EMAIL == EMAIL).first()
        if utilisateur and check_password_hash(utilisateur.MDP, MDP):
            return utilisateur
        return None

    @staticmethod
    def ajout(EMAIL, MDP):
        """
        Permet l'ajout d'un utilisateur à partir d'un  mail et d'un mot de passe fournis

        Les deux arguments sont obligatoires

        Parameters
        ----------
        mail : str, required
            Le mail fourni par le client
        password : str, required
            Le mot de passe fourni par le client

        Returns
        -------
        app.models.users.Users
            Une instance de la classe Users et True si l'identification est un succès, sinon retourne false et l'erreur.
        """
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
    def get_user_by_id(id):
        return Utilisateurs.query.get(int(id))
        
    def __repr__(self):
        return f"<Utilisateurs {dict(USER_ID=self.USER_ID, EMAIL=self.EMAIL, MDP=self.MDP)}>"

