import streamlit as st
import random
import time

st.set_page_config(page_title="数字ハンター", layout="centered")

# =====================
# 設定
# =====================
NUM_COUNT = 5
TIME_LIMIT = 30  # 秒

# =====================
# ルール生成
# =====================
def generate_rule():
    rule_type = random.choice(["random", "ordered"])

    if rule_type == "random":
        numbers = random.sample(range(1, 20), NUM_COUNT)
        rule_description = "好きな順に全ての数字をタップせよ"
        correct_sequence = numbers  # 任意順OK

    elif rule_type == "ordered":
        start = random.randint(1, 10)
        ordered = [start + i for i in range(NUM_COUNT)]
        if random.choice([True, False]):
            ordered.reverse()
            rule_description = "数字を大きい順にタップせよ"
        else:
            rule_description = "数字を小さい順にタップせよ"
        numbers = ordered.copy()
        random.shuffle(numbers)
        correct_sequence = ordered

    return {
        "rule_type": rule_type,
        "numbers": numbers,
        "correct_sequence": correct_sequence,
        "description": rule_description
    }

# =====================
# セッション状態の初期化
# =====================
if "rule" not in st.session_state:
    st.session_state.rule = generate_rule()
    st.session_state.selected = []
    st.session_state.tap_index = 0
    st.session_state.cleared = False
    st.session_state.start_time = time.time()
    st.session_state.end_time = None
    st.session_state.score = 0

rule = st.session_state.rule
elapsed_time = int(time.time() - st.session_state.start_time)
remaining_time = TIME_LIMIT - elapsed_time

st.title("🎯 数字ハンター")
st.subheader(rule["description"])

# タイマー表示
if remaining_time > 0 and not st.session_state.cleared:
    st.info(f"⏱ 残り時間: {remaining_time} 秒")
else:
    if not st.session_state.cleared:
        st.error("🕒 タイムオーバー！ゲームオーバー")
        if st.button("もう一度遊ぶ"):
            st.session_state.rule = generate_rule()
            st.session_state.selected = []
            st.session_state.tap_index = 0
            st.session_state.cleared = False
            st.session_state.start_time = time.time()
            st.session_state.end_time = None
            st.session_state.score = 0
        st.stop()

cols = st.columns(NUM_COUNT)
for i, num in enumerate(rule["numbers"]):
    if num not in st.session_state.selected:
        if cols[i].button(str(num), key=f"btn_{num}") and not st.session_state.cleared:
            if rule["rule_type"] == "random":
                st.session_state.selected.append(num)
                st.session_state.score += 10
            elif rule["rule_type"] == "ordered":
                expected = rule["correct_sequence"][st.session_state.tap_index]
                if num == expected:
                    st.session_state.selected.append(num)
                    st.session_state.tap_index += 1
                    st.session_state.score += 10
                else:
                    st.session_state.score -= 5  # ミスで減点

if len(st.session_state.selected) == NUM_COUNT:
    if not st.session_state.cleared:
        st.session_state.cleared = True
        st.session_state.end_time = time.time()
        time_taken = int(st.session_state.end_time - st.session_state.start_time)
        bonus = max(TIME_LIMIT - time_taken, 0)
        st.session_state.score += bonus

    st.success("🎉 クリア！")
    st.markdown(f"✅ あなたのスコア: **{st.session_state.score} 点**")
    if st.button("もう一度遊ぶ"):
        st.session_state.rule = generate_rule()
        st.session_state.selected = []
        st.session_state.tap_index = 0
        st.session_state.cleared = False
        st.session_state.start_time = time.time()
        st.session_state.end_time = None
        st.session_state.score = 0
