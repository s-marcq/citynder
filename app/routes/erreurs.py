from ..app import app, db
from flask import render_template

@app.errorhandler(404)
def not_found_error(error):
    """
    Route permettant de gérer l'erreur 400.

    Returns
    -------
    template
        Retourne le template de l'erreur 404.
    """

    return render_template('erreurs/404.html'), 404

@app.errorhandler(500)
@app.errorhandler(503)
def internal_error(error):
    """
    Route permettant de gérer les erreurs 500 et 503.

    Returns
    -------
    template
        Retourne le template de l'erreur 500.
    """
    db.session.rollback()
    return render_template('erreurs/500.html'), 500