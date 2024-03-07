import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config():
    DEBUG = os.environ.get("DEBUG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO=os.environ.get("SQLALCHEMY_ECHO")
    RESOURCES_PER_PAGE = str(os.environ.get("RESOURCES_PER_PAGE")) # Marina : j'ai modifié en de int à str sinon erreur au moment du lancement de l'application 
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLE = os.environ.get("WTF_CSRF_ENABLE")
