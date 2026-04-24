import streamlit as st
import pandas as pd
from analytics.macro_engine import run_macro
from analytics.abbank_engine import run_abbank
from analytics.treasury_engine import run_treasury
from analytics.signal_engine import run_signal
from analytics.recommendation_engine import run_reco
from analytics.report_engine import build_ceo_brief

st.set_page_config(page_title="ABBank BI System", layout="wide")
st.title("ABBank Business Intelligence System")

macro = run_macro()
abbank = run_abbank()
treasury = run_treasury()
signals = run_signal(macro, abbank, treasury)
reco = run_reco(signals)
brief = build_ceo_brief(macro, abbank, treasury, reco)

latest_m = macro.iloc[-1]
latest_a = abbank.iloc[-1]
latest_t = treasury.iloc[-1]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Macro score", f"{latest_m['macro_score']:.1f}")
c2.metric("ABBank score", f"{latest_a['abbank_score']:.1f}")
c3.metric("LDR", f"{latest_a['ldr']:.2f}%")
c4.metric("DV01", f"{latest_t['dv01']:.2f} tỷ/bp")

tabs = st.tabs(["Executive", "Macro", "ABBank", "Treasury", "Strategy"])
with tabs[0]:
    st.subheader("CEO Morning Brief")
    st.text(brief)
    st.subheader("Top signals")
    st.dataframe(pd.DataFrame(reco), use_container_width=True)
with tabs[1]:
    st.line_chart(macro.set_index("date")[["cpi", "vnibor_on", "macro_score"]])
    st.dataframe(macro.tail(12), use_container_width=True)
with tabs[2]:
    st.line_chart(abbank.set_index("date")[["nim", "casa", "ldr", "npl", "abbank_score"]])
    st.dataframe(abbank.tail(12), use_container_width=True)
with tabs[3]:
    st.line_chart(treasury.set_index("date")[["duration", "dv01", "loss_200bps_pct_capital"]])
    st.dataframe(treasury.tail(12), use_container_width=True)
with tabs[4]:
    st.dataframe(pd.DataFrame(reco), use_container_width=True)
