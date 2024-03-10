from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='statics')
app.config.from_object(Config)
Bootstrap(app)


db = SQLAlchemy(app)

login = LoginManager(app)
login.login_message = "Veuillez vous connecter pour accèder à cette page."
login.login_message_category = "info"

from .routes import recherche, users, erreurs, panier, page_finale, accueil, graphiques
