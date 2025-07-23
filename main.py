import streamlit as st
from PIL import Image
import time
import os

st.set_page_config(page_title="시향이 때리기", layout="centered")

# 기본 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'is_hit' not in st.session_state:
    st.session_state.is_hit = False

# 게임 설정
GAME_DURATION = 30  # seconds

# 이미지 로딩
normal_img = Image.open("shihyang_normal.png")
hit_img = Image.open("shihyang_hit.png")

st.title("💢 시향이 때리기 게임")
st.write("30초 안에 최대한 많이 시향이를 때려보세요!")

# 게임 시작 버튼
if st.button("게임 시작", type="primary"):
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False

# 게임 로직
if st.session_state.start_time and not st.session_state.game_over:
    elapsed = time.time() - st.session_state.start_time
    remaining = GAME_DURATION - int(elapsed)
    
    st.markdown(f"⏱️ 남은 시간: **{remaining}초**")
    st.markdown(f"👊 점수: **{st.session_state.score}점**")

    if remaining <= 0:
        st.session_state.game_over = True
        st.session_state.start_time = None
    else:
        # 이미지 클릭 시 점수 증가
        clicked = st.button("👉 시향이 때리기")
        if clicked:
            st.session_state.score += 1
            st.session_state.is_hit = True
        else:
            st.session_state.is_hit = False

        st.image(hit_img if st.session_state.is_hit else normal_img, width=300)

# 게임 종료
if st.session_state.game_over:
    st.markdown(f"🎉 게임 종료! 당신의 점수는 **{st.session_state.score}점**입니다.")
