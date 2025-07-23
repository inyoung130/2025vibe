import streamlit as st
import random
from PIL import Image
import os
import time

# 과일 매핑
fruit_names = {
    "딸기": "strawberry.png",
    "바나나": "banana.png",
    "자두": "plum.png",
    "라임": "lime.png"
}

fruit_emojis = {
    "딸기": "🍓",
    "바나나": "🍌",
    "자두": "🍇",  # 자두는 포도 이모지로 대체
    "라임": "🍈"   # 라임은 멜론 이모지로 대체
}

# 세션 초기화
if "cards" not in st.session_state:
    fruits = list(fruit_names.keys())
    st.session_state.cards = [(random.choice(fruits), random.randint(1, 5)) for _ in range(40)]
    random.shuffle(st.session_state.cards)
    st.session_state.shown = []
    st.session_state.turn = "player"
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.message = ""

st.title("🎮 할리갈리 vs AI (이미지 없는 버전도 OK)")

# 카드 내기
def play_card(player):
    if st.session_state.cards:
        card = st.session_state.cards.pop()
        st.session_state.shown.append(card)
        st.session_state.message = f"{player}가 카드를 냈습니다: {card[0]} {card[1]}개"
    else:
        st.session_state.message = "📦 카드가 모두 소진되었습니다!"

# 종 치기
def check_bell(player):
    counter = {}
    for fruit, count in st.session_state.shown:
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

# 사용자 턴
if st.session_state.turn == "player":
    st.subheader("🧍 당신의 턴입니다")
    if st.button("🃏 카드 내기"):
        play_card("플레이어")
        st.session_state.turn = "ai"
        time.sleep(0.5)

    if st.button("⏰ 종 치기!"):
        check_bell("player")

# AI 턴
if st.session_state.turn == "ai":
    st.subheader("🤖 AI의 턴입니다")
    time.sleep(1)
    play_card("AI")

    counter = {}
    for fruit, count in st.session_state.shown:
        counter[fruit] = counter.get(fruit, 0) + count
    found_five = any(c == 5 for c in counter.values())

    time.sleep(1.5)
    ai_reacts = False
    if found_five:
        ai_reacts = random.random() < 0.8  # 80% 확률로 종침
    else:
        ai_reacts = random.random() < 0.1  # 10% 확률로 실수

    if ai_reacts:
        check_bell("ai")

    st.session_state.turn = "player"

# 카드 출력
st.markdown("### 📌 최근 카드들:")
latest = st.session_state.shown[-5:]
for fruit, count in reversed(latest):
    path = f"images/{fruit_names[fruit]}"
    if os.path.exists(path):
        images = [Image.open(path) for _ in range(count)]
        st.image(images, width=50)
    else:
        emoji = fruit_emojis.get(fruit, "❓")
        st.write(f"**{fruit} {count}개**  →  {emoji * count}")

# 점수
col1, col2 = st.columns(2)
col1.metric("🧍 당신 점수", st.session_state.player_score)
col2.metric("🤖 AI 점수", st.session_state.ai_score)

# 메시지 출력
if st.session_state.message:
    st.info(st.session_state.message)
