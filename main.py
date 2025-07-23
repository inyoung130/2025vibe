import streamlit as st
import random
import time

# 과일 설정
fruit_emojis = {
    "딸기": "🍓",
    "바나나": "🍌",
    "포도": "🍇",
    "멜론": "🍈"
}
fruit_list = list(fruit_emojis.keys())

# 세션 초기화
if "cards" not in st.session_state:
    st.session_state.cards = [(random.choice(fruit_list), random.randint(1, 5)) for _ in range(40)]
    random.shuffle(st.session_state.cards)
    st.session_state.shown = []  # (과일, 개수, 낸 사람)
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.message = ""
    st.session_state.ready_for_bell = False  # 종 칠 수 있는 시점인지

st.set_page_config(page_title="할리갈리", layout="centered")
st.title("🎮 할리갈리 vs AI (자연스러운 텀 추가)")

# 카드 내기
def play_card(player_label):
    if st.session_state.cards:
        fruit, count = st.session_state.cards.pop()
        st.session_state.shown.append((fruit, count, player_label))
        return f"{player_label}가 카드를 냈습니다: {fruit} {count}개"
    else:
        return "📦 카드가 모두 소진되었습니다!"

# 종 치기
def check_bell(player):
    counter = {}
    for fruit, count, _ in st.session_state.shown:
        counter[fruit] = counter.get(fruit, 0) + count
    correct = any(c == 5 for c in counter.values())
    if correct:
        if player == "player":
            st.session_state.player_score += 1
            st.session_state.message = "✅ 당신이 정답! 점수 +1"
        else:
            st.session_state.ai_score += 1
            st.session_state.message = "🤖 AI가 종을 정확히 쳤습니다! 점수 +1"
    else:
        if player == "player":
            st.session_state.player_score -= 1
            st.session_state.message = "❌ 당신이 틀렸습니다! 점수 -1"
        else:
            st.session_state.ai_score -= 1
            st.session_state.message = "😅 AI가 실수로 종을 쳤습니다. 점수 -1"

# 종 버튼
def bell_button():
    st.markdown("### 🔔 가운데 종을 눌러주세요!")
    if st.session_state.ready_for_bell and st.button("🔔 종 치기!", use_container_width=True):
        check_bell("player")
        st.session_state.ready_for_bell = False

# 턴 진행: 당신 카드 → AI 카드 (딜레이 포함)
if st.button("🃏 내 차례! 카드 내기"):
    st.session_state.message = play_card("플레이어")

    # 🕒 AI 반응 텀 추가
    with st.spinner("🤖 AI가 카드를 고민 중..."):
        time.sleep(random.uniform(0.8, 1.5))
    st.session_state.message += "\n" + play_card("AI")

    # 종 반응 판단
    counter = {}
    for fruit, count, _ in st.session_state.shown:
        counter[fruit] = counter.get(fruit, 0) + count
    found_five = any(c == 5 for c in counter.values())

    time.sleep(1.0)  # 종 칠지 말지 결정 시간
    ai_reacts = False
    if found_five:
        ai_reacts = random.random() < 0.8
    else:
        ai_reacts = random.random() < 0.1

    if ai_reacts:
        check_bell("ai")
        st.session_state.ready_for_bell = False
    else:
        st.session_state.ready_for_bell = True

# 카드 시각화
def show_card(player_label):
    card = next((c for c in reversed(st.session_state.shown) if c[2] == player_label), None)
    if card:
        fruit, count, _ = card
        emoji = fruit_emojis.get(fruit, "❓")
        st.markdown(f"#### {player_label}가 낸 카드")
        st.markdown(f"<h3 style='text-align:center'>{emoji * count}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; font-size:20px'>{fruit} × {count}</div>", unsafe_allow_html=True)
    else:
        st.info(f"{player_label}가 아직 카드를 내지 않았습니다.")

st.markdown("## 🃏 현재 카드 상태")
col1, col2 = st.columns(2)
with col1:
    show_card("플레이어")
with col2:
    show_card("AI")

# 종 치기 버튼
bell_button()

# 점수
col1, col2 = st.columns(2)
col1.metric("🧍 당신 점수", st.session_state.player_score)
col2.metric("🤖 AI 점수", st.session_state.ai_score)

# 메시지
if st.session_state.message:
    st.info(st.session_state.message)
