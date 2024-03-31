def clean_arg(arg):

    """
        Fonction qui transforme les chaînes de caractère vides en None, sinon elle les retourne telles quelles.

        Parameters
        ----------
        arg : required
            argument de la fonction : chaîne à vérifier et transformer.

        Returns
        -------
        arg
            Retourne l'argument si ce n'est pas une chaîne vide.
        None
            None si la chaîne est vide
    """

    if arg == "":
        return None
    else:
        return arg


def normalisation_champs_texte(champs) :
    """
        Fonction de normalisation des champs texte pour les valeurs par défaut du formulaire lorsque que la valeur None ne peut être traitée.
        
        Parameters
        ----------
        champs : required
            champs à modifier.

        Returns
        -------
        champs
            Retourne la chaîne contenue dans le champs si la valeur n'est pas nulle.
        une chaîne de caractères vide
            si le contenu du champs était nul
    """
    if champs == None :
        return ""
    else :
        return champs