
def calculer_loyer_m2_min(loyer_min, loyer_max, surface_min, surface_max):
    if loyer_min != "":
        if surface_min != "" and surface_min != "0":
            return int(loyer_min) / int(surface_min)
        elif surface_max != "" and surface_max != "0":
            return int(loyer_min) / int(surface_max)
        else:
            return None
    else:
        return 0

def calculer_loyer_m2_max(loyer_min, loyer_max, surface_min, surface_max):
    if loyer_max != "":
        if surface_max != "" and surface_max != "0":
            return int(loyer_max) / int(surface_max)
        elif surface_min != "" and surface_min != "0":
            return int(loyer_max) / int(surface_min)
        else:
            return None
    else:
        return float('inf')


# Fonction de normalisation des champs texte lorsque "None doit être affiché"
def normalisation_champs_texte(champs) :
        if champs == None :
            return ""
        else :
            return champs
