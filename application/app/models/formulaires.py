from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
import re


class Recherche(FlaskForm):
    # Loyer
    appartement = BooleanField("appartement")
    maison = BooleanField("maison")
    appart_et_maison = BooleanField("appart_et_maison")
    loyer_min = TextAreaField("loyer_min", validators=[Optional()])
    loyer_max = TextAreaField("loyer_max", validators=[Optional()])
    surface_min = TextAreaField("surface_min", validators=[Optional()]) # supprimé : Integerfield, render_kw={"placeholder": "Entrez un nombre entier"}
    surface_max = TextAreaField("surface_max", validators=[Optional()])

    # Nature
    montagne = BooleanField("montagne") 
    littoral = BooleanField("littoral") 
    PNR = BooleanField("PNR") 

    # Culture
    musée = BooleanField("musée") 
    opera = BooleanField("opera")
    cinema = BooleanField("cinema") 
    theatre = BooleanField("theatre")
    bibliothèque = BooleanField("bibliothèque")

    #Sports
    foot = BooleanField("foot")
    piscine = BooleanField("piscine")
    rando = BooleanField("rando")
    sportco = BooleanField("sportco")
    escalade = BooleanField("escalade")
    petanque = BooleanField("petanque")

    # Commerces 
    com_alim = SelectField('com_alim', choices=[('', ''),('0', '0'),('1', '1'), ('2 à 5', '2 à 5'), ('5 à 10', '5 à 10'), ('plus de 10', 'plus de 10')])
    com_non_alim = SelectField('com_non_alim', choices=[('', ''),('0', '0'),('1', '1'), ('2 à 5', '2 à 5'), ('5 à 10', '5 à 10'), ('plus de 10', 'plus de 10')])

    # Population
    pop = SelectField('pop', choices=[('', ''),('moins de 1 000', 'moins de 1 000 habitants'),('1 000 à 5 000', '1 000 à 5 000 habitants'), ('5 000 à 10 000', '5 000 à 10 000 habitants'), ('plus de 10 000', 'plus de 10 000 habitants')])

    # Région et département
    # with app.app_context():
    #     choix_departements = [('', '')]
    #     choix_regions = [('', '')]
    #     for choix in Commune.query.with_entities(Commune.DEPARTEMENT).distinct():
    #         choix_departements.append((choix[0], choix[0]))
    #     for choix in Commune.query.with_entities(Commune.REGION).distinct():
    #         choix_regions.append((choix[0], choix[0]))
    # departement = SelectMultipleField("departement", choices=sorted(choix_departements))
    # region = SelectMultipleField("region", choices=sorted(choix_regions))

    # Validation
    def validation(self):
        if self.loyer_max.data or self.loyer_min.data:
            if self.surface_min.data is None and self.surface_max.data is None:
                raise ValidationError('Veuillez remplir le champ de surface.')
        for champs in [self.surface_max.data, self.surface_min.data, self.loyer_max.data, self.loyer_min.data]:
            if champs!="":
                if not champs.isnumeric() :
                    raise Exception("Veuillez entrer des nombres entiers positifs dans les champs surface et loyer")
                elif int(champs)<=0:
                    raise Exception("Veuillez entrer des nombres entiers positifs dans les champs surface et loyer")

        if self.loyer_max.data !="" :
            if int(self.loyer_max.data) <= int(self.loyer_min.data) :
                raise Exception("Le loyer minimal doit être inférieur au loyer maximal")
            
        if self.surface_max.data !="":
            if int(self.surface_max.data) <= int(self.surface_min.data) :
                raise Exception("La surface minimale doit être inférieur à la surface maximale")

        return "ok"


    
    
class AjoutUtilisateur(FlaskForm):
    mail = StringField("mail", validators=[DataRequired(message="Champ mail obligatoire"),
        Email(message="Le mail saisi n'est pas valide")])
    password = PasswordField("password", validators=[DataRequired(message="Champ mot de passe obligatoire"),
        Length(min=6, message="Le mot de passe fait moins de 6 caractères"),
        EqualTo('password_confirm', message='Les mots de passe doivent être identiques')])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired(message="Confirmation de mot de passe obligatoire")])

    def validate_password(self, password):
        if re.search( "[0-9]", password.data) and re.search("[a-z]", password.data) and re.search("[A-Z]", password.data):
            pass
        else:
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre, une minuscule et une majuscule")

class Connexion(FlaskForm):
    mail = StringField("mail", validators=[DataRequired(message="Champ mail obligatoire"),
        Email(message="Le mail saisi n'est pas valide")])
    password = PasswordField("password", validators=[DataRequired(message="Champ mot de passe obligatoire")])