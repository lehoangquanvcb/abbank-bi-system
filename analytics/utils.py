import pandas as pd
import urllib.parse

SHEET_ID = "1kdosejgGgYiUusTZNCGKXmyXP45g89rp4esZ61dri8g"

def read_sheet(sheet_name: str) -> pd.DataFrame:
    sheet_name_encoded = urllib.parse.quote(sheet_name)
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={sheet_name_encoded}"
    )

    df = pd.read_csv(url)
    df = df.dropna(how="all")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

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
