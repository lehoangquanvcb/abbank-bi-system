import numpy as np
from .utils import read_sheet

def run_macro():
    df = read_sheet("INPUT_MACRO")
    df["fx_mom_pct"] = df["usd_vnd"].pct_change().fillna(0) * 100
    df["credit_deposit_gap"] = df["credit_growth"] - df["deposit_growth"]
    df["liquidity_pressure"] = np.where(df["vnibor_on"] >= 5.5, 100, np.where(df["vnibor_on"] >= 4.5, 65, 30))
    df["inflation_pressure"] = np.where(df["cpi"] >= 4.5, 100, np.where(df["cpi"] >= 3.5, 65, 30))
    df["macro_score"] = (100 - 0.35*df["liquidity_pressure"] - 0.35*df["inflation_pressure"] - 0.30*df["fx_mom_pct"].abs()*15).clip(0,100)
    return df
