from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
import re


class Recherche(FlaskForm):
    # Loyer
    appartement = BooleanField("appartement")
    maison = BooleanField("maison")
    appart_et_maison = BooleanField("appart_et_maison")
    loyer_min = IntegerField("loyer_min", validators=[Optional(), DataRequired()],render_kw={"placeholder": "Entrez un nombre entier"})
    loyer_max = IntegerField("loyer_max", validators=[Optional(), DataRequired()],render_kw={"placeholder": "Entrez un nombre entier"})
    surface_min = IntegerField("surface_min", validators=[Optional(), DataRequired()],render_kw={"placeholder": "Entrez un nombre entier"})
    surface_max = IntegerField("surface_max", validators=[Optional(), DataRequired()],render_kw={"placeholder": "Entrez un nombre entier"})

    # Nature
    montagne = BooleanField("montagne") 
    littoral = BooleanField("littoral") 
    PNR = BooleanField("PNR") 


    # Culture
    musée = BooleanField("musée") 

    # Validation
    def validation(self):
        if self.loyer_max.data or self.loyer_min.data:
            if self.surface_min.data is None and self.surface_max.data is None:
                raise ValidationError('Veuillez remplir le champ de surface.')
        return "ok"


# <exemples>
class InsertionPays(FlaskForm):
    code_pays =  StringField("code_pays", validators=[]) 
    nom_pays =  StringField("nom_pays", validators=[])
    type = SelectField('type', choices=[('', ''),('sovereign', 'Souverain'), ('dependency', 'Dépendance'), ('ocean', 'Océan'), ('other', 'Autre')])
    introduction =  TextAreaField("code_pays", validators=[]) 
    ressources = SelectMultipleField('ressources', choices=[('', ''),('PET','petroleum'),('NAT','natural gas'),('IRO','iron ore'),('PHO','phosphates'),('URA','uranium'),('LEA','lead'),('ZIN','zinc'),('DIA','diamonds'),('COP','copper'),('FEL','feldspar'),('GOL','gold'),('BAU','bauxite'),('NIC','nickel'),('SAL','salt'),('SOD','soda ash'),('POT','potash'),('COA','coal'),('SIL','silver'),('LIM','limestone'),('MAR','marble'),('TIM','timber'),('RAR','rare earth oxides'),('PEA','peat'),('COB','cobalt'),('PLA','platinum'),('VAN','vanadium'),('ARA','arable land'),('HYD','hydropower'),('NIO','niobium'),('TAN','tantalum'),('TIN','tin'),('TUN','tungsten'),('KAO','kaolin'),('FIS','fish (Lake Chad)'),('SAN','sand and gravel'),('MAG','magnesium'),('MAN','manganese'),('OIL','oil'),('BAS','basalt rock'),('CLA','clay'),('GYP','gypsum'),('GRA','granite'),('PUM','pumice'),('TAL','talc'),('ASB','asbestos'),('ZIR','zircon'),('RUB','rubber'),('COC','cocoa beans'),('COF','coffee'),('PAL','palm oil'),('GEM','gemstones'),('FLU','fluorspar'),('WIL','wildlife'),('WAT','water'),('BUI','building stone'),('CHR','chromite'),('QUA','quartz'),('TAR','tar sands'),('SEM','semiprecious stones'),('MIC','mica'),('AND','and bauxite'),('NOT','note'),('MOL','molybdenum'),('HAR','hardwoods'),('MET','methane'),('CIN','cinnamon trees'),('ANT','antimony'),('LOB','lobster'),('LIK','likely oil reserves'),('LIT','lithium'),('CAD','cadmium'),('FOR','forests'),('EME','emeralds'),('ICE','icefish'),('TOO','toothfish'),('NON','none'),('CRA','crayfish'),('ALU','alumina'),('MIN','mineral sands'),('OPA','opals'),('BEA','beaches'),('NEG','NEGL'),('GEO','geothermal power'),('TRO','tropical fruit'),('CHI','chicle'),('CAL','calcium carbonate'),('<P>','<p>fish'),('MAH','mahogany forests'),('SHR','shrimp'),('ASP','asphalt'),('SPI','spiny lobster'),('CON','conch'),('PRO','protected harbors'),('HOT','hot springs</p>'),('PLE','pleasant climate'),('MER','mercury'),('BIS','bismuth'),('BRO','brown coal'),('SUL','sulfur'),('PRE','precious stones'),('HEL','helium'),('ARS','arsenic'),('GAL','gallium'),('GER','germanium'),('HAF','hafnium'),('TEL','tellurium'),('SEL','selenium'),('STR','strontium'),('LIG','lignite'),('CAR','carbonates'),('DOL','dolomitic limestone'),('CHA','chalk'),('PYR','pyrites'),('STO','stone'),('BAR','barite'),('SEA','sea mud'),('SOF','soft coal'),('WHA','whales'),('FRE','French Guiana'),('CRO','cropland'),('LOW','low-grade iron ore'),('AMB','amber'),('GAS','gas'),('SEP','sepiolite'),('SLA','slate'),('SHA','shale oil'),('ROC','rock salt'),('BOR','borate'),('PER','perlite'),('BER','beryllium'),('NIT','nitrates'),('SQU','squid'),('SPH','sphagnum moss'),('OTH','other minerals'),('SUG','sugarcane'),('SCE','scenic beauty'),('POO','poor quality coal')])
    continent = SelectField('ressources', choices=[('', ''),('Europe', 'Europe'), ('Asia', 'Asie'), ('Africa', 'Afrique'), ('Oceania', 'Océanie'), ('North America', 'Amérique du Nord')])
# </exemples>
    

# Utilisateurs (à garder et probablement modifier)
    
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