from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "ABBank_BI_Master_Template.xlsx"

def read_sheet(sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(WORKBOOK, sheet_name=sheet_name, engine="openpyxl", skiprows=2)
    df = df.dropna(how="all")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df

def latest_row(df: pd.DataFrame) -> pd.Series:
    return df.sort_values("date").iloc[-1] if "date" in df.columns else df.iloc[-1]

def traffic_light(value: float, yellow: float, red: float, high_is_bad: bool = True) -> str:
    if high_is_bad:
        if value >= red:
            return "Đỏ"
        if value >= yellow:
            return "Vàng"
        return "Xanh"
    if value <= red:
        return "Đỏ"
    if value <= yellow:
        return "Vàng"
    return "Xanh"
