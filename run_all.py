from analytics.macro_engine import run_macro
from analytics.abbank_engine import run_abbank
from analytics.treasury_engine import run_treasury
from analytics.signal_engine import run_signal
from analytics.recommendation_engine import run_reco
from analytics.report_engine import build_ceo_brief

if __name__ == "__main__":
    macro = run_macro()
    abbank = run_abbank()
    treasury = run_treasury()
    signals = run_signal(macro, abbank, treasury)
    reco = run_reco(signals)
    brief = build_ceo_brief(macro, abbank, treasury, reco)
    print("=== ABBANK CEO MORNING BRIEF ===")
    print(brief)
