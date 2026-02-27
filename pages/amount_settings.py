import streamlit as st

st.title("⚙️ 設定 (Settings)")

# session_state（アプリ全体で共有する変数）の初期化
if "WATER_PER_PERSON" not in st.session_state:
    st.session_state.WATER_PER_PERSON = 150
if "SCOOP_WEIGHT" not in st.session_state:
    st.session_state.SCOOP_WEIGHT = 10

st.write("コーヒーの抽出に関する基本設定を変更できます。")

# ユーザーが変更できる入力欄
new_water = st.number_input(
    "1人あたりの湯量 (ml)", 
    value=st.session_state.WATER_PER_PERSON, 
    step=10
)
new_scoop = st.number_input(
    "スプーン1杯の豆量 (g)", 
    value=st.session_state.SCOOP_WEIGHT, 
    step=1
)

# 保存ボタン
if st.button("設定を保存"):
    st.session_state.WATER_PER_PERSON = new_water
    st.session_state.SCOOP_WEIGHT = new_scoop
    st.success("設定を保存しました！メインページに戻って確認してください。")