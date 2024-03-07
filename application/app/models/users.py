from ..app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

class Users(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    mail = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @staticmethod
    def identification(prenom, password):
        utilisateur = Users.query.filter(Users.prenom == prenom).first()
        if utilisateur and check_password_hash(utilisateur.password, password):
            return utilisateur
        return None

    @staticmethod
    def ajout(mail, password):
        erreurs = []
        if not mail:
            erreurs.append("Le mail est vide")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe est vide ou trop court")

        unique = Users.query.filter(
            db.or_(Users.mail == mail)
        ).count()
        if unique > 0:
            erreurs.append("Cette adresse mail existe déjà")

        if len(erreurs) > 0:
            return False, erreurs
        utilisateur = Users(
            mail=mail,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]
        
    def get_id(self):
        return self.id
        
    @login.user_loader
    def get_user_by_id(id):
        return Users.query.get(int(id))