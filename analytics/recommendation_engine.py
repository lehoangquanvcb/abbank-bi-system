def run_reco(signals):
    recos = []

    for s in signals:
        signal = s["signal"]
        level = s["level"]

        if signal == "VNIBOR spike":
            action = "Giảm duration, ưu tiên bond ngắn hạn, hạn chế tăng DV01 mới."
            impact = "Giảm rủi ro MTM khi lãi suất thị trường tăng."
            owner = "Treasury"

        elif signal == "FX pressure":
            action = "Theo dõi trạng thái USD, giảm open position, cân nhắc hedge."
            impact = "Giảm rủi ro tỷ giá và áp lực thanh khoản ngoại tệ."
            owner = "Treasury/ALM"

        elif signal == "LDR high":
            action = "Tăng CASA campaign, kiểm soát tăng trưởng tín dụng, ưu tiên khách hàng yield tốt."
            impact = "Giảm áp lực funding cost và bảo vệ NIM."
            owner = "Finance/Business"

        elif signal == "NPL risk":
            action = "Rà soát phân khúc rủi ro, tăng early warning, hạn chế giải ngân nhóm yếu."
            impact = "Giảm áp lực trích lập và bảo vệ ROA/ROE."
            owner = "Risk"

        elif signal == "Treasury stress loss":
            action = "Giảm DV01, đặt stop-loss, tái cân bằng duration bucket."
            impact = "Giảm nguy cơ vượt khẩu vị rủi ro Treasury."
            owner = "Treasury/Risk"

        else:
            action = "Theo dõi thêm."
            impact = "Chưa có hành động cụ thể."
            owner = "TBD"

        recos.append({
            "level": level,
            "signal": signal,
            "action": action,
            "impact": impact,
            "owner": owner
        })

    priority = {"Đỏ": 1, "Vàng": 2, "Xanh": 3}
    return sorted(recos, key=lambda x: priority.get(x["level"], 9))
