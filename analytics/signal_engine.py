from .utils import latest_row, traffic_light

def run_signal(macro, abbank, treasury):
    m = latest_row(macro)
    a = latest_row(abbank)
    t = latest_row(treasury)
    signals = [
        {"signal":"VNIBOR spike", "value":float(m["vnibor_on"]), "level":traffic_light(float(m["vnibor_on"]), 4.5, 5.5), "comment":"Áp lực thanh khoản ngắn hạn."},
        {"signal":"FX pressure", "value":abs(float(m["fx_mom_pct"])), "level":traffic_light(abs(float(m["fx_mom_pct"])), 1.5, 3.0), "comment":"Biến động tỷ giá theo tháng."},
        {"signal":"LDR high", "value":float(a["ldr"]), "level":traffic_light(float(a["ldr"]), 85, 90), "comment":"Áp lực huy động/tín dụng."},
        {"signal":"NPL risk", "value":float(a["npl"]), "level":traffic_light(float(a["npl"]), 2.5, 3.0), "comment":"Chất lượng tài sản cần theo dõi."},
        {"signal":"Treasury stress loss", "value":float(t["loss_200bps_pct_capital"]), "level":traffic_light(float(t["loss_200bps_pct_capital"]), 3, 5), "comment":"Stress loss so với vốn Treasury."},
    ]
    return signals
