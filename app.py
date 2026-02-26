import streamlit as st
import time
import math

# ==========================================
# 0. パスワードロック機能（追加部分）
# ==========================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.set_page_config(page_title="Coffee Timer Login", page_icon="☕", layout="centered")
    st.markdown("""
        <style>
            .stApp { background-color: #FFFDF9 !important; color: #5D4037 !important; }
            h1 { color: #5D4037 !important; text-align: center; }
            button[kind="primary"] { background-color: #8D6E63 !important; color: #FFFFFF !important; border: none !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🔒 Coffee Timer")
    st.markdown('<p style="color: #4b3832; font-weight: bold;">合言葉を入力してください (Please enter the password)</p>', unsafe_allow_html=True)
    password = st.text_input("Pass", type="password", label_visibility="collapsed")
    if st.button("Login", type="primary", use_container_width=True):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("パスワードが違います (Incorrect password)")
    st.stop()  # 認証されるまで、これより下のコードは一切実行・表示されません

# ==========================================
# ★ アプリの設定値（定数）
# ==========================================
WATER_PER_PERSON = 160      # 1人あたりの湯量 (ml)（人数指定時）
MAX_BREW_TIME_SEC = 210     # 全体の抽出時間の上限 (秒) = 3分30秒
IDEAL_STEP_TIME_SEC = 45    # 1工程あたりの理想的な待機時間 (秒)
SCOOP_WEIGHT = 12.0         # 計量スプーン1杯の重さ (g)
BASE_WATER_RATIO = 15.0     # 基本の抽出比率 (粉1gに対する湯量)

# ==========================================
# 1. ページ設定とカスタムCSS
# ==========================================
st.set_page_config(page_title="Coffee Timer", page_icon="☕", layout="centered")

st.markdown("""
<style>
    /* 全体テーマ */
    .stApp { background-color: #FFFDF9 !important; color: #5D4037 !important; }
    h1, h2, h3, span, div, label { color: #5D4037 !important; }
    
    /* 入力フォーム */
    input[type="number"] { background-color: #F5EFEB !important; color: #5D4037 !important; border-color: #D7CCC8 !important; }
    div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child { background-color: #8D6E63 !important; border-color: #8D6E63 !important; }
    
    /* 言語切り替えボタン用の調整 */
    .lang-switcher { display: flex; justify-content: flex-end; margin-bottom: -20px; }
    
    /* スタートボタンの強調表示 */
    button[kind="primary"] { 
        background-color: #8D6E63 !important; 
        color: #FFFFFF !important; 
        border: none !important; 
        border-radius: 8px !important;
        padding: 15px 0 !important;
        transition: all 0.3s; 
    }
    button[kind="primary"] * { color: #FFFFFF !important; }
    button[kind="primary"] p {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
    }
    button[kind="primary"]:hover { 
        background-color: #6D4C41 !important; 
        transform: scale(1.02);
    }
    
    /* タイマー周辺 */
    .timer-container { text-align: center; margin-top: 10px; }
    .next-step-text { text-align: center; color: #8D6E63; font-size: 1.1rem; margin-top: 15px; font-weight: bold; }
    .completion-message { font-size: 1.8rem; font-weight: bold; color: #8D6E63; text-align: center; padding: 30px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 言語設定と翻訳テキスト（多言語対応）
# ==========================================
col_title, col_lang = st.columns([3, 1])
with col_title:
    st.title("☕️ Coffee Timer")
with col_lang:
    st.markdown('<div class="lang-switcher">', unsafe_allow_html=True)
    lang = st.radio("Language", ["日本語", "English"], horizontal=True, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

is_ja = (lang == "日本語")

# テキスト辞書
t = {
    "method_water": "湯量で指定 (ml)" if is_ja else "By Water (ml)",
    "method_people": "人数で指定 (人)" if is_ja else "By People",
    "water_label": "抽出したい量 (ml)" if is_ja else "Total Water (ml)",
    "people_label": f"人数 (1人={WATER_PER_PERSON}ml)" if is_ja else f"People ({WATER_PER_PERSON}ml/person)",
    "calc_caption": "※合計湯量: {water} ml" if is_ja else "* Total water: {water} ml",
    "strength": "お好みの濃さ" if is_ja else "Strength",
    "str_light": "浅め" if is_ja else "Light",
    "str_normal": "ふつう" if is_ja else "Normal",
    "str_strong": "深め" if is_ja else "Strong",
    "metric_water": "💧 お湯の量" if is_ja else "💧 Water",
    "metric_beans": "🫘 コーヒー豆" if is_ja else "🫘 Beans",
    "scoops": "約 {scoops} 杯" if is_ja else "~{scoops} scoops",
    "timer_title": "⏱️ ドリップタイマー" if is_ja else "⏱️ Drip Timer",
    "sound": "🔊 音を鳴らす" if is_ja else "🔊 Play Sound",
    "start": "▶️ ドリップを開始する" if is_ja else "▶️ Start Dripping",
    "sec": "秒" if is_ja else "sec",
    "target": "目標:" if is_ja else "Target:",
    "add": "(今回注ぐ量: +{add} ml)" if is_ja else "(Add: +{add} ml)",
    "next": "次の工程： {name} (+{add} ml)" if is_ja else "Next: {name} (+{add} ml)",
    "last": "これが最後の工程です" if is_ja else "This is the final step!",
    "done": "🎉 抽出完了！<br>美味しいコーヒーをどうぞ。" if is_ja else "🎉 Brewing Complete!<br>Enjoy your coffee.",
    "credit": "※本ツールは、粕谷哲氏考案の<a href='https://www.youtube.com/watch?v=lJNPp-onikk' target='_blank' style='color: #8D6E63; text-decoration: underline;'>「4:6メソッド」</a>の抽出理論を参考に作成しています。" if is_ja else "*This tool is inspired by the <a href='https://www.youtube.com/watch?v=lJNPp-onikk' target='_blank' style='color: #8D6E63; text-decoration: underline;'>\"4:6 method\"</a> created by Tetsu Kasuya."
}

st.write("---")

# ==========================================
# 3. ロジック部分（計算関数）
# ==========================================
def calculate_custom_46(total_water: float, strength: str) -> dict:
    water_ratio_small = BASE_WATER_RATIO * 0.8
    threshold_small = 250
    ratio = water_ratio_small if total_water <= threshold_small else BASE_WATER_RATIO
    
    beans_weight = total_water / ratio
    scoops = beans_weight / SCOOP_WEIGHT
    
    water_40 = total_water * 0.4
    pour_1 = beans_weight * 2.0
    pour_2 = water_40 - pour_1
    pours = [pour_1, pour_2]
    
    divisions = 2 if strength == t["str_light"] else (4 if strength == t["str_strong"] else 3)
    water_60 = total_water - water_40
    pour_60_each = water_60 / divisions
    for _ in range(divisions):
        pours.append(pour_60_each)
        
    timeline = []
    cumulative_water = 0
    
    # 言語に応じたステップ名
    if is_ja:
        step_names = ["1投目", "2投目"] + [f"{i+3}投目" for i in range(divisions)]
    else:
        step_names = ["Pour 1", "Pour 2"] + [f"Pour {i+3}" for i in range(divisions)]
    
    total_steps = len(pours)
    duration_per_step = min(IDEAL_STEP_TIME_SEC, MAX_BREW_TIME_SEC // total_steps)
    
    for i, pour in enumerate(pours):
        pour_int = int(round(pour))
        cumulative_water += pour_int
        timeline.append({
            "ステップ": step_names[i],
            "注ぐ量 (ml)": pour_int,
            "スケール目標 (ml)": cumulative_water,
            "待機時間 (秒)": duration_per_step
        })
        
    return {
        "beans_g": beans_weight,
        "scoops": scoops,
        "timeline": timeline
    }

# ==========================================
# 4. 円形タイマー描画用の関数
# ==========================================
def get_circular_timer_html(progress, duration, current_step_name, target_ml, add_ml):
    size = 280
    stroke_width = 14
    radius = (size - stroke_width) / 2
    circumference = 2 * math.pi * radius
    stroke_dashoffset = circumference * (1 - progress)
    remaining_sec = int(duration * progress)

    html = f"""
<div class="timer-container">
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
<circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#EFEBE9" stroke-width="{stroke_width}" />
<circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#8D6E63" stroke-width="{stroke_width}" stroke-dasharray="{circumference}" stroke-dashoffset="{stroke_dashoffset}" stroke-linecap="round" transform="rotate(-90 {size/2} {size/2})" style="transition: stroke-dashoffset 1s linear;" />
<text x="50%" y="30%" text-anchor="middle" dominant-baseline="middle" font-size="18" fill="#5D4037">{current_step_name}</text>
<text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" font-size="64" font-weight="bold" fill="#8D6E63">{remaining_sec} <tspan font-size="24">{t['sec']}</tspan></text>
<text x="50%" y="70%" text-anchor="middle" dominant-baseline="middle" font-size="20" fill="#5D4037">{t['target']} <tspan font-size="32" font-weight="bold">{target_ml}</tspan> ml</text>
<text x="50%" y="85%" text-anchor="middle" dominant-baseline="middle" font-size="16" fill="#8D6E63">{t['add'].format(add=add_ml)}</text>
</svg>
</div>
"""
    return html.strip()

# ==========================================
# 5. 音声再生用のHTML
# ==========================================
sound_html = """
<iframe srcdoc="<script>
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'sine';
  osc.frequency.setValueAtTime(880, ctx.currentTime);
  gain.gain.setValueAtTime(0.1, ctx.currentTime);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.15);
</script>" width="0" height="0" style="display:none; border:none;"></iframe>
"""

# ==========================================
# 6. UI構築部分
# ==========================================
col1, col2 = st.columns(2)

with col1:
    input_mode = st.radio("指定方法", [t["method_water"], t["method_people"]], horizontal=True, label_visibility="collapsed")
    if input_mode == t["method_water"]:
        total_water = st.number_input(t["water_label"], min_value=100, max_value=1000, value=200, step=10)
    else:
        num_people = st.number_input(t["people_label"], min_value=1, max_value=6, value=1, step=1)
        total_water = num_people * WATER_PER_PERSON
        st.caption(t["calc_caption"].format(water=int(total_water)))

with col2:
    strength = st.radio(t["strength"], options=[t["str_light"], t["str_normal"], t["str_strong"]], index=1, horizontal=True)

result = calculate_custom_46(total_water, strength)

st.write("")

# --- 結果表示 ---
scoops_str = t["scoops"].format(scoops=round(result['scoops'], 1))
beans_g_str = f"({round(result['beans_g'], 1)} g)"

st.markdown(f"""
<div style="display: flex; justify-content: space-around; background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #EFEBE9; box-shadow: 0 2px 8px rgba(93, 64, 55, 0.05); margin-bottom: 20px;">
    <div style="text-align: center;">
        <div style="color: #8D6E63; font-size: 1rem; margin-bottom: 5px;">{t['metric_water']}</div>
        <div style="color: #5D4037; font-size: 1.8rem; font-weight: bold;">{int(total_water)} ml</div>
    </div>
    <div style="text-align: center;">
        <div style="color: #8D6E63; font-size: 1rem; margin-bottom: 5px;">{t['metric_beans']}</div>
        <div style="color: #5D4037; font-size: 1.8rem; font-weight: bold;">{scoops_str}</div>
        <div style="color: #8D6E63; font-size: 1.2rem; font-weight: normal;">{beans_g_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. タイマーエリアとクレジットの配置
# ==========================================
timer_area = st.container()

st.write("---")

st.markdown(f"""
<div style="text-align: center; margin-top: 40px; font-size: 0.8rem; color: #BCAAA4;">
    {t['credit']}
</div>
""", unsafe_allow_html=True)

with timer_area:
    st.subheader(t["timer_title"])
    sound_on = st.checkbox(t["sound"], value=False)

    if st.button(t["start"], type="primary", use_container_width=True):
        timer_placeholder = st.empty()
        next_step_placeholder = st.empty()
        sound_placeholder = st.empty()
        
        timeline = result["timeline"]
        total_steps = len(timeline)

        for i, step_info in enumerate(timeline):
            current_step_name = step_info["ステップ"]
            target_ml = step_info["スケール目標 (ml)"]
            add_ml = step_info["注ぐ量 (ml)"]
            duration = step_info["待機時間 (秒)"]
            
            if i + 1 < total_steps:
                next_step_name = timeline[i+1]["ステップ"]
                next_add_ml = timeline[i+1]["注ぐ量 (ml)"]
                next_info = t["next"].format(name=next_step_name, add=next_add_ml)
            else:
                next_info = t["last"]

            for elapsed_sec in range(duration + 1):
                progress = 1.0 - (elapsed_sec / duration)
                timer_html = get_circular_timer_html(progress, duration, current_step_name, target_ml, add_ml)
                timer_placeholder.markdown(timer_html, unsafe_allow_html=True)
                next_step_placeholder.markdown(f"<div class='next-step-text'>{next_info}</div>", unsafe_allow_html=True)
                
                if elapsed_sec == 0 and sound_on:
                    sound_placeholder.markdown(sound_html, unsafe_allow_html=True)
                elif elapsed_sec == 1:
                    sound_placeholder.empty()
                    
                time.sleep(1)

        timer_placeholder.markdown(f"<div class='completion-message'>{t['done']}</div>", unsafe_allow_html=True)
        next_step_placeholder.empty()
        st.balloons()
