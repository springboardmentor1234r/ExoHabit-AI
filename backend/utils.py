import pandas as pd

def preprocess_input(data):
    """
    Converts incoming JSON data into model-ready DataFrame
    """

    features = [
        "pl_rade",
        "pl_bmasse",
        "pl_dens",
        "pl_eqt",
        "pl_orbper",
        "st_teff",
        "st_lum",
        "st_met"
    ]

    values = [
        float(data.get("pl_rade", 0)),
        float(data.get("pl_bmasse", 0)),
        float(data.get("pl_dens", 0)),
        float(data.get("pl_eqt", 0)),
        float(data.get("pl_orbper", 0)),
        float(data.get("st_teff", 0)),
        float(data.get("st_lum", 0)),
        float(data.get("st_met", 0))
    ]

    df = pd.DataFrame([values], columns=features)

    return df
