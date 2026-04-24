from .utils import read_sheet

def run_abbank():
    df = read_sheet("INPUT_ABBANK")
    df["growth_score"] = (50 + df["loan_growth"] * 3).clip(0,100)
    df["funding_score"] = (100 - (df["ldr"] - 80).clip(lower=0)*3 + df["casa"]).clip(0,100)
    df["asset_quality_score"] = (100 - df["npl"]*20).clip(0,100)
    df["abbank_score"] = 0.30*df["growth_score"] + 0.40*df["funding_score"] + 0.30*df["asset_quality_score"]
    return df
