import streamlit as st
import random

# 초기화
if "cards" not in st.session_state:
    fruits = ["딸기", "바나나", "자두", "라임"]
    st.session_state.cards = []
    for _ in range(30):
        fruit = random.choice(fruits)
        count = random.randint(1, 5)
        st.session_state.cards.append((fruit, count))
    random.shuffle(st.session_state.cards)
    st.session_state.shown = []
    st.session_state.score = 0
    st.session_state.message = ""

st.title("🍓 할리갈리 게임")
st.subheader("🃏 카드를 보고 종을 쳐보세요!")

# 현재 카드 상태
if st.button("다음 카드 내기"):
    if st.session_state.cards:
        st.session_state.shown.append(st.session_state.cards.pop())
        st.session_state.message = ""
    else:
        st.session_state.message = "카드가 모두 소진되었습니다!"

# 종 치기
if st.button("⏰ 종 치기!"):
    fruit_counter = {}
    for fruit, count in st.session_state.shown:
        fruit_counter[fruit] = fruit_counter.get(fruit, 0) + count
    correct = any(count == 5 for count in fruit_counter.values())
    if correct:
        st.session_state.score += 1
        st.session_state.message = "✅ 정답! 점수 +1"
    else:
        st.session_state.score -= 1
        st.session_state.message = "❌ 오답! 점수 -1"

# 공개된 카드
st.markdown("### 📌 현재까지 공개된 카드:")
for fruit, count in reversed(st.session_state.shown[-5:]):  # 최근 카드 5장 표시
    st.write(f"→ {fruit} {count}개")

# 점수
st.metric("현재 점수", st.session_state.score)

# 메시지
if st.session_state.message:
    st.info(st.session_state.message)
