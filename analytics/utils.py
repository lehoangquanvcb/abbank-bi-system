import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

@st.cache_data(ttl=600)
def read_sheet(sheet_name: str) -> pd.DataFrame:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet=sheet_name)
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
