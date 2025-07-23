import streamlit as st
import random
import time

# 이모지 매핑
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
    st.session_state.player_card = None
    st.session_state.ai_card = None
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.ready_for_bell = False
    st.session_state.message = ""

st.set_page_config(page_title="할리갈리", layout="centered")
st.title("🎮 할리갈리 vs AI")

# 종 치기 판정
def check_bell(player):
    total = {}
    for who, card in [("플레이어", st.session_state.player_card), ("AI", st.session_state.ai_card)]:
        if card:
            fruit, count = card
            total[fruit] = total.get(fruit, 0) + count
    found_five = any(v == 5 for v in total.values())

    if found_five:
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

    st.session_state.ready_for_bell = False

# 종 치기 버튼 (항상 표시)
st.markdown("### 🔔 종 치기!")
if st.button("🔔 종 치기!", use_container_width=True):
    if st.session_state.ready_for_bell:
        check_bell("player")
    else:
        st.session_state.message = "⛔ 지금은 종을 칠 수 없습니다!"

# 카드 내기 버튼
if st.button("🃏 내 차례! 카드 내기"):
    st.session_state.message = ""

    # 1. 당신 카드
    if st.session_state.cards:
        st.session_state.player_card = st.session_state.cards.pop()
    else:
        st.session_state.player_card = None

    # 2. 당신 카드 먼저 보여주기
    st.markdown("## 🧍 당신 카드")
    if st.session_state.player_card:
        fruit, count = st.session_state.player_card
        emoji = fruit_emojis[fruit]
        st.markdown(f"<h3 style='text-align:center'>{emoji * count}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'>{fruit} × {count}</div>", unsafe_allow_html=True)
    else:
        st.warning("📦 카드가 모두 소진되었습니다!")

    # 3. 딜레이 후 AI 카드
    with st.spinner("🤖 AI가 카드를 고민 중..."):
        time.sleep(random.uniform(1.2, 2.0))  # 사람같은 반응 속도

    if st.session_state.cards:
        st.session_state.ai_card = st.session_state.cards.pop()
    else:
        st.session_state.ai_card = None

    st.markdown("## 🤖 AI 카드")
    if st.session_state.ai_card:
        fruit, count = st.session_state.ai_card
        emoji = fruit_emojis[fruit]
        st.markdown(f"<h3 style='text-align:center'>{emoji * count}</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'>{fruit} × {count}</div>", unsafe_allow_html=True)
    else:
        st.warning("📦 카드가 모두 소진되었습니다!")

    # 4. AI 종 반응 (실수 확률 낮춤)
    total = {}
    for card in [st.session_state.player_card, st.session_state.ai_card]:
        if card:
            fruit, count = card
            total[fruit] = total.get(fruit, 0) + count
    found_five = any(v == 5 for v in total.values())

    time.sleep(1.0)
    if found_five and random.random() < 0.8:
        check_bell("ai")
    elif not found_five and random.random() < 0.05:  # 오류 확률 ↓
        check_bell("ai")
    else:
        st.session_state.ready_for_bell = True

# 카드 상태 표시
st.markdown("## 🃏 현재 카드")
cols = st.columns(2)
with cols[0]:
    st.markdown("#### 🧍 당신")
    if st.session_state.player_card:
        fruit, count = st.session_state.player_card
        emoji = fruit_emojis[fruit]
        st.markdown(f"<div style='text-align:center; font-size:32px'>{emoji * count}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center'>{fruit} × {count}</div>", unsafe_allow_html=True)
with cols[1]:
    st.markdown("#### 🤖 AI")
    if st.session_state.ai_card:
        fruit, count = st.session_state.ai_card
        emoji = fruit_emojis[fruit]
        st.markdown(f"<div style='text-align:center; font-size:32px'>{emoji * count}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center'>{fruit} × {count}</div>", unsafe_allow_html=True)

# 점수
st.markdown("---")
sc1, sc2 = st.columns(2)
sc1.metric("🧍 당신 점수", st.session_state.player_score)
sc2.metric("🤖 AI 점수", st.session_state.ai_score)

# 메시지
if st.session_state.message:
    st.info(st.session_state.message)
