import math
import ezdxf

def generer_dessin_dxf(r, filename="poteau_BA_rendu.dxf"):
    """Génère automatiquement un plan CAO au format DXF (Coupe + Elévation)"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # Création des calques selon les chartes graphiques AutoCAD
    doc.layers.new(name='BETON', dxfattribs={'color': 7})  # Blanc/Noir
    doc.layers.new(name='ACIER LONG', dxfattribs={'color': 1})  # Rouge
    doc.layers.new(name='ETRIERS', dxfattribs={'color': 3})  # Vert
    doc.layers.new(name='TEXTES', dxfattribs={'color': 2})  # Jaune

    # Extraction et conversion des dimensions en mm
    b = r["b"] * 10
    h = r["h"] * 10
    H_mm = r["H"] * 1000
    c = r["cnom"]

    try:
        phi_l = float(r["choix_armature"].split("HA")[-1])
    except:
        phi_l = 12.0

    r_barre = phi_l / 2
    phi_etrier = r["phi_min"]

    # --- VUE 1 : COUPE TRANSVERSALE ---
    if r["type_section"] == "Rectangulaire":
        h_elevation = h
        # Dessin du contour béton
        msp.add_lwpolyline([(0, 0), (b, 0), (b, h), (0, h)], close=True, dxfattribs={'layer': 'BETON'})
        # Dessin du cadre d'étrier intérieur
        msp.add_lwpolyline([
            (c, c), (b - c, c), (b - c, h - c), (c, h - c)
        ], close=True, dxfattribs={'layer': 'ETRIERS'})

        # Positionnement des 4 aciers longitudinaux aux angles
        dist = c + phi_etrier + r_barre
        coins = [(dist, dist), (b - dist, dist), (b - dist, h - dist), (dist, h - dist)]
        for coin in coins:
            msp.add_circle(coin, r_barre, dxfattribs={'layer': 'ACIER LONG'})

        msp.add_text(f"Coupe A-A | b={b:.0f}mm x h={h:.0f}mm",
                     dxfattribs={'layer': 'TEXTES', 'height': 15}).set_placement((0, h + 30))
        msp.add_text(f"Armatures: {r['choix_armature']}",
                     dxfattribs={'layer': 'TEXTES', 'height': 12}).set_placement((0, -30))

    else:  # Cas d'une section Circulaire
        D = r["diam_section"] * 10
        h_elevation = D
        # Dessin du contour béton rond (centré pour l'alignement)
        msp.add_circle((D / 2, D / 2), D / 2, dxfattribs={'layer': 'BETON'})
        # Étrier circulaire
        r_etrier = (D / 2) - c
        msp.add_circle((D / 2, D / 2), r_etrier, dxfattribs={'layer': 'ETRIERS'})

        # Répartition de 4 barres principales à 90°
        dist_c = r_etrier - r_barre
        angles = [0, 90, 180, 270]
        for ang in angles:
            rad = math.radians(ang)
            cx = D / 2 + dist_c * math.cos(rad)
            cy = D / 2 + dist_c * math.sin(rad)
            msp.add_circle((cx, cy), r_barre, dxfattribs={'layer': 'ACIER LONG'})

        msp.add_text(f"Coupe Section Circulaire D={D:.0f}mm",
                     dxfattribs={'layer': 'TEXTES', 'height': 15}).set_placement((0, D + 30))
        msp.add_text(f"Armatures: {r['choix_armature']}",
                     dxfattribs={'layer': 'TEXTES', 'height': 12}).set_placement((0, -30))

    # --- VUE 2 : VUE LONGITUDINALE (ELEVATION) ---
    x_offset = b + 300 if r["type_section"] == "Rectangulaire" else (D + 300)

    # Contour extérieur
    msp.add_lwpolyline([
        (x_offset, 0), (x_offset + H_mm, 0),
        (x_offset + H_mm, h_elevation), (x_offset, h_elevation)
    ], close=True, dxfattribs={'layer': 'BETON'})

    # Lignes d'aciers longitudinaux
    dist_l = c + phi_etrier + r_barre
    msp.add_line((x_offset, dist_l), (x_offset + H_mm, dist_l), dxfattribs={'layer': 'ACIER LONG'})
    msp.add_line((x_offset, h_elevation - dist_l), (x_offset + H_mm, h_elevation - dist_l), dxfattribs={'layer': 'ACIER LONG'})

    # Génération et répartition des lignes d'étriers transversaux
    s_espacement = r["s_cl_tmax"]
    x_position = x_offset + c
    while x_position <= (x_offset + H_mm - c):
        msp.add_line((x_position, c), (x_position, h_elevation - c), dxfattribs={'layer': 'ETRIERS'})
        x_position += s_espacement

    msp.add_text(f"Vue Longitudinale (Hauteur H = {r['H']} m)",
                 dxfattribs={'layer': 'TEXTES', 'height': 15}).set_placement((x_offset, h_elevation + 30))
    msp.add_text(f"Etriers espacement max: {s_espacement:.0f} mm",
                 dxfattribs={'layer': 'TEXTES', 'height': 12}).set_placement((x_offset, -30))

    doc.saveas(filename)