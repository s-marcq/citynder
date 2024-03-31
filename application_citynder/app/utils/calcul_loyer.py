
def calculer_loyer_m2_min(loyer_min, loyer_max, surface_min, surface_max):
    """
        Fonction qui calcule le loyer a mètre carré minimal voulu par l'utilisateur en None.

        Parameters
        ----------
        loyer_min : required
            loyer minimum rentré par l'utilisateur
        loyer_max : required
            loyer maximum
        surface_min : required
            surface minimum souhaitée
        surface_max : required
            suface maximum souhaitée

        Returns
        -------
        le loyer minimal au mètre carré
    """
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
    """
        Fonction qui calcule le loyer a mètre carré maximal voulu par l'utilisateur en None.

        Parameters
        ----------
        loyer_min : required
            loyer minimum rentré par l'utilisateur
        loyer_max : required
            loyer maximum
        surface_min : required
            surface minimum souhaitée
        surface_max : required
            suface maximum souhaitée

        Returns
        -------
        le loyer maximal au mètre carré
    """
    if loyer_max != "":
        if surface_max != "" and surface_max != "0":
            return int(loyer_max) / int(surface_max)
        elif surface_min != "" and surface_min != "0":
            return int(loyer_max) / int(surface_min)
        else:
            return None
    else:
        return float('inf')



