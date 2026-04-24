from .utils import latest_row

def build_ceo_brief(macro, abbank, treasury, reco):
    m, a, t = latest_row(macro), latest_row(abbank), latest_row(treasury)
    lines = []
    lines.append(f"Ngày {m['date'].date()}: CPI {m['cpi']:.2f}%, VNIBOR ON {m['vnibor_on']:.2f}%, USD/VND {m['usd_vnd']:,.0f}.")
    lines.append(f"ABBank score {a['abbank_score']:.1f}; LDR {a['ldr']:.2f}%, NPL {a['npl']:.2f}%, NIM {a['nim']:.2f}%.")
    lines.append(f"Treasury: duration {t['duration']:.2f}, DV01 {t['dv01']:.2f} tỷ/bp, loss 200bps {t['stress_loss_200bps']:.1f} tỷ.")
    lines.append("Hành động ưu tiên:")
    for r in reco[:3]:
        lines.append(f"- [{r['level']}] {r['signal']}: {r['action']} ({r['owner']})")
    return "\n".join(lines)
