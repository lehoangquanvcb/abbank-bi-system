import streamlit as st
import pandas as pd

from analytics.macro_engine import run_macro
from analytics.abbank_engine import run_abbank
from analytics.treasury_engine import run_treasury
from analytics.signal_engine import run_signal
from analytics.recommendation_engine import run_reco
from analytics.report_engine import build_ceo_brief

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="ABBank BI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== STYLE =====
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.metric-card {
    background: #0E1117;
    border: 1px solid #2A2F3A;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
}

.metric-title {
    color: #A0A7B4;
    font-size: 13px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 24px;
    font-weight: 700;
}

.metric-note {
    color: #A0A7B4;
    font-size: 12px;
}

.alert-red {
    background: #4A1111;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}

.alert-yellow {
    background: #4A3B11;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}

.alert-green {
    background: #123D25;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}

[data-testid="stAppViewContainer"] {
    background-color: #080B10;
}
</style>
""", unsafe_allow_html=True)

# ===== VIEW MODE =====
view_mode = st.radio(
    "View mode",
    ["Desktop", "Mobile"],
    horizontal=True,
    index=0
)

is_mobile = view_mode == "Mobile"

# ===== COMPONENT =====
def card(title, value, note=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def alert_box(signal, level, action):
    css = "alert-green"
    if level == "Đỏ":
        css = "alert-red"
    elif level == "Vàng":
        css = "alert-yellow"

    st.markdown(f"""
    <div class="{css}">
        <b>{level} | {signal}</b><br>
        {action}
    </div>
    """, unsafe_allow_html=True)

# ===== LOAD DATA =====
macro = run_macro()
abbank = run_abbank()
treasury = run_treasury()

signals = run_signal(macro, abbank, treasury)
reco = run_reco(signals)
brief = build_ceo_brief(macro, abbank, treasury, reco)

latest_m = macro.iloc[-1]
latest_a = abbank.iloc[-1]
latest_t = treasury.iloc[-1]

# ===== HEADER =====
st.title("🏦 ABBank BI Dashboard")

# ===== TABS =====
tab1, tab2, tab3, tab4 = st.tabs([
    "CEO",
    "Market",
    "ABBank",
    "Action"
])

# ===== TAB 1: CEO =====
with tab1:
    st.subheader("Executive Snapshot")

    if is_mobile:
        c1, c2 = st.columns(2)
        with c1:
            card("Macro Score", f"{latest_m['macro_score']:.1f}")
        with c2:
            card("ABBank Score", f"{latest_a['abbank_score']:.1f}")

        c3, c4 = st.columns(2)
        with c3:
            card("LDR", f"{latest_a['ldr']:.2f}%")
        with c4:
            card("NPL", f"{latest_a['npl']:.2f}%")

        c5, c6 = st.columns(2)
        with c5:
            card("DV01", f"{latest_t['dv01']:.2f}")
        with c6:
            card("Stress Loss", f"{latest_t['stress_loss_200bps']:.0f}")

    else:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: card("Macro Score", f"{latest_m['macro_score']:.1f}")
        with c2: card("ABBank Score", f"{latest_a['abbank_score']:.1f}")
        with c3: card("LDR", f"{latest_a['ldr']:.2f}%")
        with c4: card("NPL", f"{latest_a['npl']:.2f}%")
        with c5: card("DV01", f"{latest_t['dv01']:.2f}")
        with c6: card("Stress Loss", f"{latest_t['stress_loss_200bps']:.0f}")

    st.subheader("Alerts")
    for r in reco:
        alert_box(r["signal"], r["level"], r["action"])

    st.subheader("CEO Brief")
    st.text_area("", brief, height=200)

# ===== TAB 2: MARKET =====
with tab2:
    st.subheader("Macro")

    c1, c2, c3 = st.columns(3)
    with c1: card("CPI", f"{latest_m['cpi']:.2f}%")
    with c2: card("VNIBOR", f"{latest_m['vnibor_on']:.2f}%")
    with c3: card("USD/VND", f"{latest_m['usd_vnd']:,.0f}")

    st.line_chart(
        macro.set_index("date")[["cpi", "vnibor_on", "macro_score"]].tail(24)
    )

# ===== TAB 3: ABBANK =====
with tab3:
    st.subheader("Business")

    c1, c2, c3, c4 = st.columns(4)
    with c1: card("NIM", f"{latest_a['nim']:.2f}%")
    with c2: card("CASA", f"{latest_a['casa']:.2f}%")
    with c3: card("Loan Growth", f"{latest_a['loan_growth']:.2f}%")
    with c4: card("Deposit Growth", f"{latest_a['deposit_growth']:.2f}%")

    st.line_chart(
        abbank.set_index("date")[["nim", "casa", "ldr", "npl"]].tail(24)
    )

# ===== TAB 4: ACTION =====
with tab4:
    st.subheader("Strategy")

    df = pd.DataFrame(reco)
    st.dataframe(df[["level", "signal", "action", "owner"]], use_container_width=True)

    st.subheader("Treasury Risk")
    st.line_chart(
        treasury.set_index("date")[["duration", "dv01", "loss_200bps_pct_capital"]].tail(24)
    )
