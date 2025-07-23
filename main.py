import streamlit as st
import random

st.set_page_config(page_title="점심메뉴 추천기", page_icon="🍱", layout="centered")

# 기본 메뉴 데이터
default_menus = {
    "한식": ["김치찌개", "비빔밥", "제육볶음", "된장찌개", "불고기"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "볶음밥"],
    "일식": ["스시", "우동", "라멘", "가츠동", "돈부리"],
    "양식": ["파스타", "스테이크", "피자", "햄버거", "샐러드"]
}

# 세션 상태에 메뉴 저장
if "menus" not in st.session_state:
    st.session_state.menus = default_menus.copy()

st.title("🍽️ 오늘 뭐 먹지?")

st.markdown("점심 메뉴 선택에 고민된다면 버튼을 눌러보세요!")

# 카테고리 선택
selected_categories = st.multiselect("카테고리를 선택하세요 (선택하지 않으면 전체에서 추천)", list(st.session_state.menus.keys()))

# 사용자 메뉴 추가
with st.expander("📌 내가 좋아하는 메뉴 추가하기"):
    new_menu = st.text_input("메뉴 이름 입력")
    new_category = st.selectbox("카테고리 선택", list(st.session_state.menus.keys()))
    if st.button("추가하기"):
        if new_menu:
            st.session_state.menus[new_category].append(new_menu)
            st.success(f"{new_menu} 메뉴가 {new_category} 카테고리에 추가되었어요!")

# 메뉴 추천
if st.button("✅ 점심 메뉴 추천받기!"):
    if selected_categories:
        pool = sum([st.session_state.menus[cat] for cat in selected_categories], [])
    else:
        pool = sum(st.session_state.menus.values(), [])

    if pool:
        choice = random.choice(pool)
        st.subheader(f"🥁 추천 메뉴는... **{choice}** 입니다!")
    else:
        st.warning("추천할 메뉴가 없습니다. 카테고리나 메뉴를 추가해주세요!")

# 최근 추천 내역 표시 (선택 기능)
if "history" not in st.session_state:
    st.session_state.history = []

if "choice" in locals():
    st.session_state.history.append(choice)

if st.checkbox("📜 최근 추천 메뉴 보기"):
    st.write(st.session_state.history[::-1])

