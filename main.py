import streamlit as st
import random

# 저칼로리 다이어트 메뉴 데이터 (메뉴명: 칼로리)
diet_menu = {
    "닭가슴살 샐러드": 250,
    "연어 샐러드": 300,
    "두부 샐러드": 280,
    "현미밥 + 야채볶음": 400,
    "오트밀 + 과일": 350,
    "곤약면 샐러드": 200,
    "계란 흰자 오믈렛": 220,
    "채소 스무디": 180,
    "닭가슴살 스테이크": 320,
    "저지방 요거트 + 견과류": 300,
    "토마토 달걀볶음": 270,
    "브로콜리 + 닭가슴살": 290,
    "그릭요거트 + 베리": 250,
    "계란 + 아보카도 샐러드": 310,
    "해초 샐러드": 180
}

# 세션 상태로 최근 추천 저장
if "recent" not in st.session_state:
    st.session_state.recent = []

st.title("🥗 다이어트 점심 메뉴 추천기")

st.markdown("🔍 **저칼로리 건강식**만 골라서 추천해드립니다!")

# 칼로리 제한 슬라이더
max_kcal = st.slider("🔥 최대 칼로리 한도 (kcal)", min_value=150, max_value=500, value=350)

# 추천 버튼
if st.button("🎲 추천 받기"):
    # 칼로리 필터링
    candidates = [(menu, kcal) for menu, kcal in diet_menu.items() if kcal <= max_kcal]

    # 최근 추천 제외
    available = [(menu, kcal) for menu, kcal in candidates if menu not in st.session_state.recent]

    if not available:
        st.warning("추천 가능한 메뉴가 없어요. 최근 추천 내역을 초기화할게요.")
        st.session_state.recent = []
        available = candidates

    selected_menu, selected_kcal = random.choice(available)
    st.success(f"✅ 오늘의 추천: **{selected_menu}** ({selected_kcal} kcal)")

    # 최근 추천 저장
    st.session_state.recent.append(selected_menu)
    if len(st.session_state.recent) > 5:
        st.session_state.recent.pop(0)

# 최근 추천 메뉴 보기
if st.checkbox("📜 최근 추천 보기"):
    st.write(st.session_state.recent)

# 사용자 메뉴 추가
st.markdown("---")
st.subheader("➕ 직접 메뉴 추가하기 (예: 참치샐러드:280)")
user_input = st.text_input("입력", placeholder="메뉴명:칼로리")

if user_input:
    try:
        name, kcal = user_input.split(":")
        name = name.strip()
        kcal = int(kcal.strip())
        diet_menu[name] = kcal
        st.success(f"'{name}' 메뉴가 추가되었습니다!")
    except:
        st.error("형식이 올바르지 않습니다. 예: 참치샐러드:280")
