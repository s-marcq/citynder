from flask import url_for, render_template, redirect, request, flash
from ..models.formulaires import AjoutUtilisateur, Connexion
from ..app import app, db #, login
from flask_login import login_user, current_user, logout_user

@app.route("/utilisateurs/ajout", methods=["GET", "POST"])
def ajout_utilisateur():
    return(None)
#     form = AjoutUtilisateur()

#     if form.validate_on_submit():
#         statut, donnees = Users.ajout(
#             prenom=clean_arg(request.form.get("prenom", None)),
#             mail=clean_arg(request.form.get("mail", None)),
#             password=clean_arg(request.form.get("password", None))
#         )
#         if statut is True:
#             flash("Ajout effectué", "success")
#             return redirect(url_for("accueil"))
#         else:
#             flash(",".join(donnees), "error")
#             return render_template("pages/ajout_utilisateur.html", form=form)
#     else:
#         return render_template("pages/ajout_utilisateur.html", form=form)

@app.route("/utilisateurs/connexion", methods=["GET","POST"])
def connexion():
    return(None)
#     form = Connexion()

#     if current_user.is_authenticated is True:
#         flash("Vous êtes déjà connecté", "info")
#         return redirect(url_for("accueil"))

#     if form.validate_on_submit():
#         utilisateur = Users.identification(
#             mail=clean_arg(request.form.get("mail", None)),
#             password=clean_arg(request.form.get("password", None))
#         )
#         if utilisateur:
#             flash("Connexion effectuée", "success")
#             login_user(utilisateur)
#             return redirect(url_for("accueil"))
#         else:
#             flash("Les identifiants n'ont pas été reconnus", "error")
#             return render_template("pages/connexion.html", form=form)

#     else:
#         return render_template("pages/connexion.html", form=form)

@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion():
    return(None)
#     if current_user.is_authenticated is True:
#         logout_user()
#     flash("Vous êtes déconnecté", "info")
#     return redirect(url_for("accueil"))

#login.login_view = 'connexion'
