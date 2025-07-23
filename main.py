import streamlit as st
import random

st.set_page_config(page_title="할리갈리 게임", layout="centered")

st.title("🍓 할리갈리 게임 🎲")
st.markdown("과일이 정확히 5개일 때 종을 누르세요!")

# 초기 세팅
if "players" not in st.session_state:
    st.session_state.players = []
if "cards" not in st.session_state:
    st.session_state.cards = []
if "fruit_types" not in st.session_state:
    st.session_state.fruit_types = ["🍓", "🍌", "🍇", "🍊"]
if "bell_pressed" not in st.session_state:
    st.session_state.bell_pressed = None
if "scores" not in st.session_state:
    st.session_state.scores = {}

# 플레이어 등록
with st.form("player_form"):
    player_input = st.text_input("플레이어 이름 입력")
    submit = st.form_submit_button("추가하기")
    if submit and player_input:
        if player_input not in st.session_state.players:
            st.session_state.players.append(player_input)
            st.session_state.scores[player_input] = 0

# 플레이어 목록 표시
if st.session_state.players:
    st.markdown("### 참가자")
    st.write(", ".join(st.session_state.players))
else:
    st.warning("플레이어를 추가해주세요.")

# 카드 뽑기
st.divider()
st.subheader("🃏 카드 뽑기")

cols = st.columns(len(st.session_state.players))
for idx, player in enumerate(st.session_state.players):
    with cols[idx]:
        if st.button(f"{player} 카드 내기", key=f"card_{player}"):
            fruit = random.choice(st.session_state.fruit_types)
            count = random.randint(1, 5)
            st.session_state.cards.append((player, fruit, count))
            st.session_state.bell_pressed = None  # 초기화

# 카드 보여주기
if st.session_state.cards:
    st.markdown("### 현재 카드 상태")
    for player, fruit, count in st.session_state.cards:
        st.write(f"{player}: {fruit} x {count}")

# 종 누르기
st.divider()
st.subheader("🔔 종 누르기")

for player in st.session_state.players:
    if st.button(f"{player} 종 누르기", key=f"bell_{player}"):
        if not st.session_state.bell_pressed:
            st.session_state.bell_pressed = player
            # 현재 카드의 과일 개수 총합 계산
            fruit_counter = {}
            for _, fruit, count in st.session_state.cards:
                fruit_counter[fruit] = fruit_counter.get(fruit, 0) + count
            if any(count == 5 for count in fruit_counter.values()):
                st.success(f"{player} 정답! 점수 +1")
                st.session_state.scores[player] += 1
            else:
                st.error(f"{player} 오답! 점수 -1")
                st.session_state.scores[player] -= 1
            # 카드 초기화
            st.session_state.cards = []

# 점수판
st.divider()
st.subheader("📊 점수판")
for player in st.session_state.players:
    st.write(f"{player}: {st.session_state.scores[player]}점")

# 리셋 버튼
if st.button("🔄 게임 리셋"):
    st.session_state.cards = []
    st.session_state.bell_pressed = None
    for player in st.session_state.players:
        st.session_state.scores[player] = 0
    st.success("게임이 초기화되었습니다!")
