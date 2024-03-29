# City'nder
Repository de l'application web City'nder créée dans le cadre du M2 TNAH à l'Ecole nationale des chartes (Paris, France) pour le cours de développement en Python. 

## Installation 
#### Les pré-requis sur Ubuntu: 

| Tâche                                                         | Ligne de commande dans le terminal               |
|---------------------------------------------------------------|--------------------------------------------------|
|Initialiser un git depuis le dossier en local                  |git init                                          |
|Copier le repo git depuis le dossier en local                  |git clone https://github.com/s-marcq/citynder.git |                                      |
|Installer et activer un environnement virtuel                  |pip install virtualenv : installer le package     |
|S'assurer que l'on est dans le dossier racine de l'application | pwd                                              |
|Si ce n'est pas le cas, y aller                                |cd dossier_racine/                                |
|Installer l'environnement                                      | virtualenv env -p python3                        |
|Activer l'environnement                                        | source env/bin/activate                          |
|Installer les requirements                                     |pip install -r requirements.txt                   |
|Créer un fichier .env au même niveau que le dossier app        | nano .env                                        |
|Changer les variables d'environnements                         | Copier/coller dans .env la partie ci-dessous*    |
|Lancer  l'application                                          | python run.py                                    |

*Les variables d'environnements : 
DEBUG=True ou False

SQLALCHEMY_DATABASE_URI="sqlite://///.../application/db.sqlite" # mettre ici le lien vers la bdd sur votre pc

SQLALCHEMY_ECHO=True ou False

WTF_CSRF_ENABLE=True ou False

SECRET_KEY= #écrire ici une clé secrète 

#### Pour utiliser l'application : 
Naviguez, amusez-vous et déménagez!
