from .utils import read_sheet

def run_treasury(treasury_capital=20000):
    df = read_sheet("INPUT_TREASURY")
    df["stress_loss_100bps"] = df["dv01"] * 100
    df["stress_loss_200bps"] = df["dv01"] * 200
    df["loss_200bps_pct_capital"] = df["stress_loss_200bps"] / treasury_capital * 100
    df["treasury_risk_score"] = (100 - df["loss_200bps_pct_capital"]*10 - df["duration"]*8).clip(0,100)
    df["risk_level"] = df["loss_200bps_pct_capital"].apply(lambda x: "Đỏ" if x >= 5 else ("Vàng" if x >= 3 else "Xanh"))
    return df
