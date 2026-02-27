import streamlit as st

# 1. 安全のための初期化（app.pyと同じものを記述）
if "WATER_PER_PERSON" not in st.session_state:
    st.session_state.WATER_PER_PERSON = 160
if "SCOOP_WEIGHT" not in st.session_state:
    st.session_state.SCOOP_WEIGHT = 12.0

if "lang" not in st.session_state:
    st.session_state.lang = "ja"

lang = st.session_state.lang

# 2. 多言語対応のテキスト辞書
text = {
    "ja": {
        "title": "⚙️ 抽出量設定",
        "desc": "コーヒーの抽出に関する基本設定を変更できます。",
        "water_label": "1人あたりの湯量 (ml)",
        "scoop_label": "スプーン1杯の豆量 (g)",
        "save_btn": "設定を保存",
        "success": "設定を保存しました！メインページに戻って確認してください。"
    },
    "en": {
        "title": "⚙️ Amount Settings",
        "desc": "Change the basic settings for coffee brewing.",
        "water_label": "Water per person (ml)",
        "scoop_label": "Beans per scoop (g)",
        "save_btn": "Save Settings",
        "success": "Settings saved! Return to the main page to check."
    }
}

t = text[lang]

# 3. 画面の描画
st.title(t["title"])
st.write(t["desc"])

new_water = st.number_input(
    t["water_label"], 
    value=st.session_state.WATER_PER_PERSON, 
    step=10
)
new_scoop = st.number_input(
    t["scoop_label"], 
    value=st.session_state.SCOOP_WEIGHT, 
    step=1.0
)

if st.button(t["save_btn"]):
    st.session_state.WATER_PER_PERSON = new_water
    st.session_state.SCOOP_WEIGHT = new_scoop
    st.success(t["success"])