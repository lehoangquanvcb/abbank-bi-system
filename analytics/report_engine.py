from .utils import latest_row

def build_ceo_brief(macro, abbank, treasury, reco):
    m = latest_row(macro)
    a = latest_row(abbank)
    t = latest_row(treasury)

    brief = f"""
1. Tóm tắt vĩ mô
CPI hiện ở mức {m['cpi']:.2f}%, VNIBOR ON {m['vnibor_on']:.2f}%, USD/VND {m['usd_vnd']:,.0f}. Macro score đạt {m['macro_score']:.1f} điểm.

2. Hàm ý với ngành ngân hàng
Điều kiện thanh khoản và tỷ giá đang ảnh hưởng trực tiếp tới funding cost, NIM và khẩu vị tăng trưởng tín dụng của toàn ngành.

3. Hàm ý với ABBank
ABBank hiện có LDR {a['ldr']:.2f}%, NIM {a['nim']:.2f}%, CASA {a['casa']:.2f}% và NPL {a['npl']:.2f}%. Trọng tâm quản trị là cân bằng giữa tăng trưởng tín dụng, chi phí vốn và chất lượng tài sản.

4. Treasury / Market 2
Danh mục có duration {t['duration']:.2f}, DV01 {t['dv01']:.2f} tỷ/bp. Stress loss 200bps ước tính {t['stress_loss_200bps']:.0f} tỷ VND.

5. Khuyến nghị ưu tiên
"""

    for r in reco[:5]:
        brief += f"\n- [{r['level']}] {r['signal']}: {r['action']} Tác động kỳ vọng: {r['impact']}"

    return brief.strip()
