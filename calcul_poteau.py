import math

# Constantes
DIAMETRES_STANDARDS = [8, 10, 12, 14, 16, 20, 25, 32]


def calculer_ferraillage(p, diam_etrier):
    """
    Calcule le ferraillage d'un poteau selon l'Eurocode 2.
    Lève une ValueError si une vérification géométrique ou normative échoue.
    """
    H = p["H"]
    t_sect = p["type_section"]
    NG, NQ = p["NG"], p["NQ"]
    fck, fyk = p["fck"], p["fyk"]
    b, h, a_cm = p["b"], p["h"], p["diam_section"]

    # 1. Vérifications géométriques et calcul de la section (Ac)
    if t_sect == "Rectangulaire":
        if h < b:
            raise ValueError("Section invalide : h doit être supérieur ou égal à b.")
        if H * 100 < 3 * h:
            raise ValueError("L'élément est considéré comme un voile (H < 3h).")
        if b < h / 4:
            raise ValueError("Section invalide : b doit être supérieur ou égal à h/4.")

        b_mm = b * 10
        h_mm = h * 10
        Ac = b_mm * h_mm
        i_min = min(b_mm, h_mm) / math.sqrt(12)
    else:
        a_mm = a_cm * 10
        Ac = math.pi * (a_mm ** 2) / 4
        i_min = a_mm / 4

    # 2. Calcul des efforts et matériaux
    lamb = H / (i_min / 1000)
    NEd = 1.35 * NG + 1.5 * NQ
    fcd = fck / 1.5
    fyd = fyk / 1.15
    NcRd = 0.85 * fcd * Ac

    # 3. Calcul des sections d'acier (As)
    As_calc = max((NEd * 1000 - NcRd) / fyd, 0)
    As_min = max(0.10 * NEd * 1000 / fyd, 0.002 * Ac)
    As_req = max(As_calc, As_min)

    # 4. Choix des armatures longitudinales
    nb_barres = 4
    choix_ha = None
    As_fournie = 0.0
    depassement = False

    for d in DIAMETRES_STANDARDS:
        section_4_barres = 4 * (math.pi * (d ** 2) / 4)
        if section_4_barres >= As_req:
            choix_ha = d
            As_fournie = section_4_barres
            break

    if choix_ha is None:
        choix_ha = DIAMETRES_STANDARDS[-1]
        As_fournie = 4 * (math.pi * (choix_ha ** 2) / 4)
        depassement = True

    # 5. Enrobage et armatures transversales (étriers)
    c_min_dur = 15
    c_min_b = choix_ha
    c_min = max(c_min_b, c_min_dur, 10)
    delta_c_dev = 10
    c_nom = c_min + delta_c_dev

    phi_min = max(6, choix_ha / 4)
    if diam_etrier < phi_min:
        raise ValueError(f"Étrier insuffisant : Ø{diam_etrier} mm < Ømin {phi_min:.1f} mm")

    if t_sect == "Rectangulaire":
        s_cl_tmax = min(20 * choix_ha, b_mm, 400)
    else:
        s_cl_tmax = min(20 * choix_ha, a_mm, 400)

    # 6. Vérification finale
    NRd = (NcRd + As_fournie * fyd) / 1000

    if depassement:
        verification = "NON OK (As trop grand)"
    else:
        verification = "OK" if NRd >= NEd else "NON OK"

    # Retourne le dictionnaire de résultats
    return {
        "H": H, "b": b, "h": h, "diam_section": a_cm, "NG": NG, "NQ": NQ,
        "NEd": NEd, "lambda": lamb, "Ac": Ac, "fcd": fcd, "fyd": fyd, "NcRd": NcRd,
        "As_calc": As_calc, "As_min": As_min, "As_req": As_req, "As_fournie": As_fournie,
        "nb_barres": nb_barres, "choix_armature": f"4 HA{choix_ha}", "cnom": c_nom, "NRd": NRd,
        "verification": verification, "type_section": t_sect, "s_cl_tmax": s_cl_tmax, "phi_min": phi_min
    }