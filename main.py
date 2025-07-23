import streamlit as st
import random
import time

# 🧒 🍇 🍌 🍇 🍉 🍈 🍇 🍌 
fruit_emojis = {
    "따기": "🍓",
    "바나나": "🍌",
    "포도": "🍇",
    "멜론": "🍈"
}
fruit_list = list(fruit_emojis.keys())

# 시스템 처음 해당 전체 복구
if "cards" not in st.session_state:
    st.session_state.cards = [(random.choice(fruit_list), random.randint(1, 5)) for _ in range(40)]
    random.shuffle(st.session_state.cards)
    st.session_state.player_card = None
    st.session_state.ai_card = None
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.ready_for_bell = False
    st.session_state.message = ""
    st.session_state.game_over = False
    st.session_state.nickname = ""
    st.session_state.start_time = None
    st.session_state.leaderboard = []
    st.session_state.show_rules = True

st.set_page_config(page_title="할리갈리", layout="centered")

# 닉네임 입력
if st.session_state.nickname == "":
    st.session_state.nickname = st.text_input("🎮 닉네임을 입력해주세요:", key="nickname_input")
    st.stop()

# 설명 창
if st.session_state.show_rules:
    with st.container():
        st.markdown("### 📘 게임 방법 설명")
        st.markdown("""
        **할리갈리 루르 요약 🌺**

        - 🍓, 🍌, 🍇, 🍈 네 종류의 과일 카드가 있어요.
        - 당사자와 AI가 번개로 카드를 내며 게임을 d558며,
        - 공개된 카드에서 **같은 과일이 정확히 5개** 나오면:

            👉 `🔔 종 치기` 버튼을 누르세요!

        - 올바른 경우 +1점, 틀린 경우 -1점
        - **5점 먼저 획득하면 승리!** 🎉
        - **-5점이 되면 게임 종료!** 💣

        재미가있게 플레이하세요!
        """)
        if st.button("❌ 닫기", key="hide_rules"):
            st.session_state.show_rules = False
            st.experimental_rerun()

# 타이머 시작
if st.session_state.start_time is None:
    st.session_state.start_time = time.time()

st.title(f"🌮 할리갈리 vs AI - {st.session_state.nickname} 님")

# 게임 종료 판정

def check_game_end():
    if st.session_state.player_score >= 5:
        elapsed = round(time.time() - st.session_state.start_time, 2)
        st.session_state.leaderboard.append((st.session_state.nickname, elapsed))
        st.session_state.game_over = True
        st.session_state.message = f"🎉 당신이 이겼습니다! ⏱️ {elapsed}초"
    elif st.session_state.ai_score >= 5:
        st.session_state.game_over = True
        st.session_state.message = "🤖 AI가 승리했습니다!"
    elif st.session_state.player_score <= -5 or st.session_state.ai_score <= -5:
        st.session_state.game_over = True
        st.session_state.message = "💥 점수가 -5가 되어 게임이 종료됩니다!"

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
            st.session_state.message = "🤖 AI가 정확히 종을 치였습니다! 점수 +1"
    else:
        if player == "player":
            st.session_state.player_score -= 1
            st.session_state.message = "❌ 당신이 실수! 점수 -1"
        else:
            st.session_state.ai_score -= 1
            st.session_state.message = "😅 AI가 실수로 종을 치였습니다. 점수 -1"

    st.session_state.ready_for_bell = False
    check_game_end()

# 카드 + 종 UI
st.markdown("## 🎿 현재 카드")
cols = st.columns(3)

# 당사자 카드 + 카드 내기
with cols[0]:
    st.markdown("#### 🧑 당사자")
    if st.session_state.player_card:
        fruit, count = st.session_state.player_card
        emoji = fruit_emojis[fruit]
        st.markdown(f"<div style='text-align:center; font-size:32px'>{emoji * count}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center'>{fruit} × {count}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center; font-size:32px;'>❓</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center'>카드를 내세요</div>", unsafe_allow_html=True)

    if not st.session_state.game_over:
        if st.button("🃏 카드 내기", key="play_card"):
            st.session_state.message = ""
            if st.session_state.cards:
                st.session_state.player_card = st.session_state.cards.pop()
            with st.spinner("🤖 AI가 카드를 고민 중..."):
                time.sleep(random.uniform(1.2, 2.0))
            if st.session_state.cards:
                st.session_state.ai_card = st.session_state.cards.pop()
            # AI 종 판단
            total = {}
            for card in [st.session_state.player_card, st.session_state.ai_card]:
                if card:
                    fruit, count = card
                    total[fruit] = total.get(fruit, 0) + count
            found_five = any(v == 5 for v in total.values())
            time.sleep(1.0)
            if found_five and random.random() < 0.8:
                check_bell("ai")
            elif not found_five and random.random() < 0.05:
                check_bell("ai")
            else:
                st.session_state.ready_for_bell = True

# 가운데: 종 + 종 치기 버튼
with cols[1]:
    st.markdown("#### 🔔 종")
    st.markdown("<div style='text-align:center; font-size:48px;'>🔔</div>", unsafe_allow_html=True)
    if st.button("종 치기!", key="bell", use_container_width=True):
        if st.session_state.game_over:
            st.session_state.message = "❌ 게임이 종료되었습니다."
        elif st.session_state.ready_for_bell:
            check_bell("player")
        else:
            st.session_state.message = "❌ 지금은 종을 치면 안되요!"

# 오른쪽: AI 카드
with cols[2]:
    st.markdown("#### 🤖 AI")
    if st.session_state.ai_card:
        fruit, count = st.session_state.ai_card
        emoji = fruit_emojis[fruit]
        st.markdown(f"<div style='text-align:center; font-size:32px'>{emoji * count}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center'>{fruit} × {count}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center; font-size:32px;'>❓</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center'>대기 중...</div>", unsafe_allow_html=True)

# 점수
st.markdown("---")
c1, c2 = st.columns(2)
c1.metric("🧑 당사자 점수", st.session_state.player_score)
c2.metric("🤖 AI 점수", st.session_state.ai_score)

# 메시지
if st.session_state.message:
    st.info(st.session_state.message)

# 게임 종료 이모지
if st.session_state.game_over:
    if "이겼습니다" in st.session_state.message:
        st.markdown("<h1 style='text-align:center;'>🎆🎇🎆</h1>", unsafe_allow_html=True)
    elif "-5" in st.session_state.message:
        st.markdown("<h1 style='text-align:center;'>💣💥💣</h1>", unsafe_allow_html=True)

# 사이드바 - 리더보드
with st.sidebar:
    st.markdown("## 🏆 리더보드")
    if st.session_state.leaderboard:
        sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x[1])
        for rank, (name, t) in enumerate(sorted_board, 1):
            st.write(f"{rank}. {name} — {t}초")
    else:
        st.write("게임을 승리해서 등록해보세요!")
