RULES = {
    "VNIBOR spike": ("Giữ duration ngắn; hạn chế tăng vị thế bond dài hạn", "Treasury"),
    "FX pressure": ("Theo dõi trạng thái USD; cân nhắc hedge/giảm trạng thái mở", "Treasury"),
    "LDR high": ("Kiểm soát tăng trưởng tín dụng; ưu tiên huy động CASA/kỳ hạn bền vững", "Finance/ALM"),
    "NPL risk": ("Rà soát phân khúc rủi ro; tăng cảnh báo sớm tín dụng", "Risk/Business"),
    "Treasury stress loss": ("Giảm DV01 hoặc đặt stop-loss theo vốn Treasury", "Treasury/Risk"),
}

def run_reco(signals):
    rows = []
    for s in signals:
        action, owner = RULES.get(s["signal"], ("Theo dõi thêm", "TBD"))
        rows.append({**s, "action": action, "owner": owner})
    priority = {"Đỏ": 1, "Vàng": 2, "Xanh": 3}
    return sorted(rows, key=lambda x: priority.get(x["level"], 9))
