# ABBank BI System

## Cách chạy

```bash
pip install -r requirements.txt
python run_all.py
streamlit run app.py
```

## Cấu trúc

- `ABBank_BI_Master_Template.xlsx`: file Excel master có input, process, dashboard, CEO brief.
- `analytics/`: các module tính macro score, ABBank score, Treasury stress, signal, recommendation.
- `app.py`: dashboard Streamlit bản MVP.
- `run_all.py`: chạy toàn bộ pipeline và in CEO morning brief.

## Triển khai thật

Thay dữ liệu mẫu trong các sheet `INPUT_*` bằng dữ liệu thật từ ABBank, NHNN, GSO, VBMA và peer banks.
