import streamlit as st
import pandas as pd

from analytics.macro_engine import run_macro
from analytics.abbank_engine import run_abbank
from analytics.treasury_engine import run_treasury
from analytics.signal_engine import run_signal
from analytics.recommendation_engine import run_reco
from analytics.report_engine import build_ceo_brief

try:
    from analytics.forecast_engine import run_forecast
except Exception:
    run_forecast = None


st.set_page_config(
    page_title="ABBank BI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


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

[data-testid="stHeader"] {
    background-color: #080B10;
}

h1, h2, h3 {
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)


def card(title, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def alert_box(signal, level, action):
    css = "alert-green"
    if level == "Đỏ":
        css = "alert-red"
    elif level == "Vàng":
        css = "alert-yellow"

    st.markdown(
        f"""
        <div class="{css}">
            <b>{level} | {signal}</b><br>
            {action}
        </div>
        """,
        unsafe_allow_html=True
    )


def safe_col(df, cols):
    return [c for c in cols if c in df.columns]


@st.cache_data(ttl=300)
def load_data():
    macro_df = run_macro()
    abbank_df = run_abbank()
    treasury_df = run_treasury()
    signals_data = run_signal(macro_df, abbank_df, treasury_df)
    reco_data = run_reco(signals_data)
    brief_text = build_ceo_brief(macro_df, abbank_df, treasury_df, reco_data)

    if run_forecast is not None:
        try:
            forecast_df = run_forecast(macro_df, abbank_df)
        except Exception:
            forecast_df = pd.DataFrame()
    else:
        forecast_df = pd.DataFrame()

    return macro_df, abbank_df, treasury_df, signals_data, reco_data, brief_text, forecast_df


macro, abbank, treasury, signals, reco, brief, forecast = load_data()

latest_m = macro.iloc[-1]
latest_a = abbank.iloc[-1]
latest_t = treasury.iloc[-1]

st.title("🏦 ABBank BI Dashboard")
st.caption("Macro → Industry → ABBank → Treasury → Forecast → Recommendation")

view_mode = st.radio(
    "View mode",
    ["Desktop", "Mobile"],
    horizontal=True,
    index=0
)

is_mobile = view_mode == "Mobile"

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "CEO",
    "Market",
    "ABBank",
    "Treasury",
    "Forecast",
    "Action"
])


with tab1:
    st.subheader("Executive Snapshot")

    if is_mobile:
        c1, c2 = st.columns(2)
        with c1:
            card("Macro Score", f"{latest_m.get('macro_score', 0):.1f}", "Vĩ mô / thanh khoản / tỷ giá")
        with c2:
            card("ABBank Score", f"{latest_a.get('abbank_score', 0):.1f}", "Growth / funding / asset quality")

        c3, c4 = st.columns(2)
        with c3:
            card("LDR", f"{latest_a.get('ldr', 0):.2f}%", "Áp lực huy động")
        with c4:
            card("NPL", f"{latest_a.get('npl', 0):.2f}%", "Chất lượng tài sản")

        c5, c6 = st.columns(2)
        with c5:
            card("DV01", f"{latest_t.get('dv01', 0):.2f}", "tỷ VND / 1bp")
        with c6:
            card("Stress Loss", f"{latest_t.get('stress_loss_200bps', 0):.0f}", "tỷ VND / 200bps")
    else:
        c1, c2, c3, c4, c5, c6 = st.columns(6)

        with c1:
            card("Macro Score", f"{latest_m.get('macro_score', 0):.1f}", "Macro")
        with c2:
            card("ABBank Score", f"{latest_a.get('abbank_score', 0):.1f}", "Internal")
        with c3:
            card("LDR", f"{latest_a.get('ldr', 0):.2f}%", "Funding")
        with c4:
            card("NPL", f"{latest_a.get('npl', 0):.2f}%", "Asset quality")
        with c5:
            card("DV01", f"{latest_t.get('dv01', 0):.2f}", "tỷ/bp")
        with c6:
            card("Stress Loss", f"{latest_t.get('stress_loss_200bps', 0):.0f}", "tỷ VND")

    st.subheader("Top Alerts")
    for r in reco:
        alert_box(
            r.get("signal", ""),
            r.get("level", ""),
            r.get("action", "")
        )

    st.subheader("CEO Brief")
    st.text_area("", brief, height=260)


with tab2:
    st.subheader("Market & Macro Intelligence")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("CPI", f"{latest_m.get('cpi', 0):.2f}%", "Inflation pressure")
    with c2:
        card("VNIBOR ON", f"{latest_m.get('vnibor_on', 0):.2f}%", "Liquidity pressure")
    with c3:
        card("USD/VND", f"{latest_m.get('usd_vnd', 0):,.0f}", "FX pressure")
    with c4:
        card("Credit-Deposit Gap", f"{latest_m.get('credit_deposit_gap', 0):.2f}%", "System liquidity")

    chart_cols = safe_col(macro, ["cpi", "vnibor_on", "macro_score"])
    if chart_cols:
        st.line_chart(macro.set_index("date")[chart_cols].tail(24))

    st.subheader("Macro Data")
    st.dataframe(macro.tail(12), use_container_width=True, hide_index=True)


with tab3:
    st.subheader("ABBank Business Intelligence")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("NIM", f"{latest_a.get('nim', 0):.2f}%", "Profitability")
    with c2:
        card("CASA", f"{latest_a.get('casa', 0):.2f}%", "Low-cost funding")
    with c3:
        card("Loan Growth", f"{latest_a.get('loan_growth', 0):.2f}%", "Credit expansion")
    with c4:
        card("Deposit Growth", f"{latest_a.get('deposit_growth', 0):.2f}%", "Funding growth")

    chart_cols = safe_col(abbank, ["nim", "casa", "ldr", "npl", "abbank_score"])
    if chart_cols:
        st.line_chart(abbank.set_index("date")[chart_cols].tail(24))

    st.subheader("ABBank Data")
    st.dataframe(abbank.tail(12), use_container_width=True, hide_index=True)


with tab4:
    st.subheader("Treasury & Market 2 Risk")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        card("Portfolio", f"{latest_t.get('portfolio_size', 0):,.0f}", "tỷ VND")
    with c2:
        card("Duration", f"{latest_t.get('duration', 0):.2f}", "years")
    with c3:
        card("DV01", f"{latest_t.get('dv01', 0):.2f}", "tỷ VND / bp")
    with c4:
        card("Loss 200bps", f"{latest_t.get('stress_loss_200bps', 0):,.0f}", "tỷ VND")

    chart_cols = safe_col(treasury, ["duration", "dv01", "loss_200bps_pct_capital"])
    if chart_cols:
        st.line_chart(treasury.set_index("date")[chart_cols].tail(24))

    st.subheader("Treasury Data")
    st.dataframe(treasury.tail(12), use_container_width=True, hide_index=True)


with tab5:
    st.subheader("Forecast 3 tháng tới")

    if forecast.empty:
        st.warning("Chưa có forecast_engine.py hoặc forecast chưa chạy được. Hãy thêm file analytics/forecast_engine.py.")
    else:
        st.dataframe(forecast, use_container_width=True, hide_index=True)

        if "variable" in forecast.columns and "date" in forecast.columns and "forecast" in forecast.columns:
            for var in forecast["variable"].dropna().unique():
                st.markdown(f"### {var}")
                temp = forecast[forecast["variable"] == var].copy()
                st.line_chart(temp.set_index("date")["forecast"])


with tab6:
    st.subheader("Strategic Recommendations")

    reco_df = pd.DataFrame(reco)

    display_cols = [c for c in ["level", "signal", "action", "impact", "owner"] if c in reco_df.columns]
    if display_cols:
        st.dataframe(reco_df[display_cols], use_container_width=True, hide_index=True)
    else:
        st.dataframe(reco_df, use_container_width=True, hide_index=True)

    st.subheader("Action Logic")
    st.markdown("""
    - **VNIBOR spike** → giảm duration, hạn chế tăng DV01.
    - **FX pressure** → theo dõi trạng thái USD, cân nhắc hedge.
    - **LDR high** → kiểm soát tín dụng, tăng CASA/funding bền vững.
    - **NPL risk** → rà soát phân khúc rủi ro, tăng early warning.
    - **Treasury stress loss** → giảm DV01, stop-loss, tái cân bằng bucket.
    """)
