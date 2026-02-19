REQUIRED_FIELDS = {
    "pl_rade","pl_bmasse","pl_dens","pl_eqt",
    "pl_orbper","sy_dist","st_lum",
    "st_teff","st_met","st_spectral_score"
}

def validate(data):
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        raise ValueError(f"Missing fields: {missing}")
