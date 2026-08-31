@echo off
cd /d H:\arabic-llm-gender-bias
python -m pip install -r software_dashboard\requirements.txt
python -m streamlit run software_dashboard\app.py
pause
