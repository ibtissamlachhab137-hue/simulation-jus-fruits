
def simulation(debit, ajout, concentration, temperature):

    # Données du procédé
    residus = 20          # kg/h
    y0 = 0.10             # Fraction massique en matière soluble
    yR = 0.40             # Concentration du jus ajouté
    Cp = 3.8              # kJ/(kg.K)
    lambda_v = 2300       # kJ/kg

    # 1. FILTRATION
    m1 = debit - residus
    y1 = (debit * y0) / m1

    # 2. MELANGE
    m2 = m1 + ajout
    y2 = (m1 * y1 + ajout * yR) / m2

    # 3. CHAUFFAGE
    Q3 = m2 * Cp * (temperature - 20) / 3600

    # 4. EVAPORATION
    x4 = concentration / 100

    m4 = (m2 * y2) / x4
    mv = m2 - m4

    Q4 = mv * lambda_v / 3600

    # 5. REFROIDISSEMENT
    Q5 = m4 * Cp * (80 - 25) / 3600

    # BILAN GLOBAL
    entrees = debit + ajout
    sorties = residus + mv + m4
    ecart = entrees - sorties

    # RESULTATS
    resultats = {
        "Débit après filtration (kg/h)": round(m1, 2),
        "Débit après mélange (kg/h)": round(m2, 2),
        "Concentration après mélange (%)": round(y2 * 100, 2),
        "Puissance de chauffage (kW)": round(Q3, 2),
        "Débit de vapeur évaporée (kg/h)": round(mv, 2),
        "Débit final (kg/h)": round(m4, 2),
        "Puissance d'évaporation (kW)": round(Q4, 2),
        "Puissance de refroidissement (kW)": round(Q5, 2),
        "Écart du bilan global (kg/h)": round(ecart, 2)
    }

    return resultats

