import streamlit as st
import random
import datetime
import pandas as pd

# ----------------------------
# 초기 세션 상태 설정
# ----------------------------
if "weights" not in st.session_state:
    st.session_state.weights = []

if "recent_menu" not in st.session_state:
    st.session_state.recent_menu = []

if "water_log" not in st.session_state:
    st.session_state.water_log = {}

# ----------------------------
# 기본 정보
# ----------------------------
today = datetime.date.today().isoformat()
water_goal = 2000  # 일일 목표 2000ml

if today not in st.session_state.water_log:
    st.session_state.water_log[today] = 0

# ----------------------------
# UI 시작
# ----------------------------
st.title("🏋️‍♀️ 다이어트 & 물컵 트래커")

# ----------------------------
# 물컵 기능
# ----------------------------
st.header("💧 오늘의 물컵 채우기")

# 현재 섭취량 표시
current_ml = st.session_state.water_log[today]
filled_cups = current_ml // 100
total_cups = water_goal // 100

# 시각적 물컵 표시 (🥤: 채운 컵 / ⚪: 빈 컵)
cup_display = " ".join(["🥤"] * filled_cups + ["⚪"] * (total_cups - filled_cups))
st.markdown(f"### {cup_display}")
st.write(f"총 섭취량: **{current_ml}ml / {water_goal}ml**")

# 버튼 클릭 시 100ml 추가
if st.button("💦 100ml 마시기"):
    if current_ml < water_goal:
        st.session_state.water_log[today] += 100
        st.rerun()  # UI 즉시 업데이트
    else:
        st.info("오늘 목표를 이미 달성했어요!")

# ----------------------------
# 물 섭취 기록 그래프
# ----------------------------
if st.session_state.water_log:
    st.subheader("📈 일별 물 섭취량")
    water_df = pd.DataFrame(
        list(st.session_state.water_log.items()),
        columns=["날짜", "섭취량(ml)"]
    ).set_index("날짜")
    st.bar_chart(water_df)

# ----------------------------
# 점심 추천 기능
# ----------------------------
st.markdown("---")
st.header("🥗 오늘의 저칼로리 점심 추천")

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

max_kcal = st.slider("칼로리 제한", min_value=150, max_value=500, value=350)

if st.button("🎲 메뉴 추천"):
    candidates = [(m, k) for m, k in diet_menu.items() if k <= max_kcal]
    available = [(m, k) for (m, k) in candidates if m not in st.session_state.recent_menu]

    if not available:
        st.warning("추천 가능한 메뉴가 없어요. 최근 추천 초기화됨.")
        st.session_state.recent_menu = []
        available = candidates

    menu, kcal = random.choice(available)
    st.success(f"✅ 추천 메뉴: **{menu}** ({kcal} kcal)")
    st.session_state.recent_menu.append(menu)
    if len(st.session_state.recent_menu) > 5:
        st.session_state.recent_menu.pop(0)

# ----------------------------
# 체중 기록 기능 (간단히 표시)
# ----------------------------
st.markdown("---")
st.header("📉 체중 기록 (요약)")

weight = st.number_input("현재 체중 입력 (kg)", min_value=30.0, max_value=200.0, step=0.1)

if st.button("📌 체중 저장"):
    st.session_state.weights.append((today, weight))
    st.success(f"{today} 체중 {weight}kg 기록됨")

if len(st.session_state.weights) >= 2:
    df = pd.DataFrame(st.session_state.weights, columns=["날짜", "체중"]).set_index("날짜")
    st.line_chart(df)

# ----------------------------
# 기록 보기
# ----------------------------
with st.expander("💧 전체 물 섭취 기록 보기"):
    for date, ml in st.session_state.water_log.items():
        st.write(f"{date}: {ml}ml")

with st.expander("📜 체중 기록 보기"):
    for date, wt in st.session_state.weights:
        st.write(f"{date}: {wt}kg")
