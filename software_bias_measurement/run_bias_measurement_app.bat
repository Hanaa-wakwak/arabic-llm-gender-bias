@echo off
cd /d H:\arabic-llm-gender-bias
python -m pip install -r software_bias_measurement\requirements.txt
python -m streamlit run software_bias_measurement\app.py
pause
