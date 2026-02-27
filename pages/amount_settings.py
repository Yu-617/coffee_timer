import streamlit as st

st.set_page_config(page_title="Coffee Timer - Settings", page_icon="☕", layout="centered")

# 1. 安全のための初期化（app.pyと同じものを記述）
if "WATER_PER_PERSON" not in st.session_state:
    st.session_state.WATER_PER_PERSON = 160
if "SCOOP_WEIGHT" not in st.session_state:
    st.session_state.SCOOP_WEIGHT = 12.0

if "lang" not in st.session_state:
    st.session_state.lang = "ja"

lang = st.session_state.lang

st.markdown("""
<style>
    .stApp { background-color: #FFFDF9 !important; color: #5D4037 !important; }
    h1, h2, h3, span, div, label { color: #5D4037 !important; }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    input[type="number"] { background-color: #F5EFEB !important; color: #5D4037 !important; border-color: #D7CCC8 !important; }
    button[kind="primary"] {
        background-color: #8D6E63 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 15px 0 !important;
        transition: all 0.3s;
    }
    button[kind="primary"] * { color: #FFFFFF !important; }
    button[kind="primary"] p { font-size: 1.1rem !important; font-weight: bold !important; color: #FFFFFF !important; }
    button[kind="primary"]:hover { background-color: #6D4C41 !important; transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# --- カスタムナビゲーション（サイドバー） ---
with st.sidebar:
    if st.session_state.lang == "ja":
        st.page_link("app.py", label="☕ ホーム")
        st.page_link("pages/amount_settings.py", label="⚙️ 抽出量設定")
    else:
        st.page_link("app.py", label="☕ Home")
        st.page_link("pages/amount_settings.py", label="⚙️ Settings")

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

if st.button(t["save_btn"], type="primary", use_container_width=True):
    st.session_state.WATER_PER_PERSON = new_water
    st.session_state.SCOOP_WEIGHT = new_scoop
    st.success(t["success"])