from flask import url_for, render_template, redirect, request, flash
from ..models.formulaires import AjoutUtilisateur, Connexion
from ..utils.transformations import  clean_arg
from ..models.db_citynder import Utilisateurs
from ..app import app, login
from flask_login import login_user, current_user, logout_user

@app.route("/utilisateurs/ajout", methods=["GET", "POST"])
def ajout_utilisateur():
    """
    Route permettant d'inscrire un utilisateur.

    Returns
    -------
    template
        Retourne le template ajout_utilisateur.html si l'utilisateur n'est pas inscrit/connecté.
        
    redirection
        Retourne une redirection vers l'accueil une fois l'utilisateur inscrit/connecté.
    """
    try:
        form = AjoutUtilisateur()

        if form.validate_on_submit():
            statut, donnees = Utilisateurs.ajout(
                EMAIL=clean_arg(request.form.get("mail", None)),
                MDP=clean_arg(request.form.get("password", None))
            )
            if statut is True:
                flash("Inscription terminée", "success")
                return redirect(url_for("accueil"))
            
            else:
                flash(",".join(donnees), "error")
                return render_template("pages/ajout_utilisateur.html", form=form)
        else:
            return render_template("pages/ajout_utilisateur.html", form=form)
        
    except Exception as e :
        flash("L'ajout a rencontré une erreur : "+ str(e))
        return render_template("pages/ajout_utilisateur.html", form=form)

    

@app.route("/utilisateurs/connexion", methods=["GET","POST"])
def connexion():
    """
    Route permettant de connecter l'utilisateur.

    Returns
    -------
    template
        Retourne le template connexion.html si l'utilisateur n'est pas connecté.

    redirection
        Retourne une redirection vers l'accueil une fois l'utilisateur connecté.
    """
    try:
        form = Connexion()
        
        if current_user.is_authenticated is True:
            flash("Tu es déjà connecté.e, tu as été redirigé.e vers l'accueil", "info")
            return redirect(url_for("accueil"))

        if form.validate_on_submit():
            utilisateur = Utilisateurs.identification(
                EMAIL=clean_arg(request.form.get("mail", None)),
                MDP=clean_arg(request.form.get("password", None))
            )
            if utilisateur:
                login_user(utilisateur)
                flash("Tu es connecté.e, tu as été redirigé.e vers l'accueil", "info")
                return redirect(url_for('accueil'))

            else:
                flash("Les identifiants n'ont pas été reconnus", "error")
                return render_template("pages/connexion.html", form=form)

        else:
            return render_template("pages/connexion.html", form=form)
        
    except Exception as e :
        flash("La connexion a rencontré une erreur : "+ str(e))
        return render_template("pages/connexion.html", form=form)


@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """
    Route permettant de déconnecter l'utilisateur.

    Returns
    -------
    redirection
        Retourne une redirection vers l'accueil.
    """
    try :
        if current_user.is_authenticated is True:
            logout_user()
        flash("Tu es déconnecté.e", "info")
        return redirect(url_for("accueil"))
    
    except Exception as e :
        flash("La déconnexion a rencontré une erreur : "+ str(e))
        return render_template("pages/accueil.html")


login.login_view = 'connexion'
