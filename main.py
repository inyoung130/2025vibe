import streamlit as st
import random
import datetime
import matplotlib.pyplot as plt

# ----------------------------
# 1. 다이어트 식단 데이터
# ----------------------------
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

# ----------------------------
# 2. 세션 상태 초기화
# ----------------------------
if "weights" not in st.session_state:
    st.session_state.weights = []  # [(날짜, 체중)]

if "recent_menu" not in st.session_state:
    st.session_state.recent_menu = []

# ----------------------------
# 3. 제목 및 체중 입력
# ----------------------------
st.title("🏋️‍♀️ 다이어트 트래커 & 점심 추천기")

st.header("📉 체중 입력")
weight = st.number_input("현재 체중을 입력하세요 (kg)", min_value=30.0, max_value=200.0, step=0.1)

if st.button("📌 체중 기록 저장"):
    today = datetime.date.today().isoformat()
    st.session_state.weights.append((today, weight))
    st.success(f"{today} 체중 {weight}kg 기록됨")

# ----------------------------
# 4. 체중 변화 시각화
# ----------------------------
if len(st.session_state.weights) >= 2:
    st.subheader("📊 체중 변화 추이")
    dates = [entry[0] for entry in st.session_state.weights]
    values = [entry[1] for entry in st.session_state.weights]

    fig, ax = plt.subplots()
    ax.plot(dates, values, marker='o', linestyle='-')
    ax.set_ylabel("체중 (kg)")
    ax.set_xlabel("날짜")
    ax.set_title("체중 변화 그래프")
    ax.grid(True)
    st.pyplot(fig)

    # 변화량 표시
    delta = values[-1] - values[-2]
    if delta > 0:
        st.warning(f"📈 체중이 +{delta:.1f}kg 증가했어요!")
    elif delta < 0:
        st.success(f"📉 체중이 {abs(delta):.1f}kg 감량됐어요!")
    else:
        st.info("체중 변화가 없어요.")

# ----------------------------
# 5. 다이어트 점심 추천
# ----------------------------
st.markdown("---")
st.header("🥗 오늘의 저칼로리 점심 추천")

max_kcal = st.slider("칼로리 제한", min_value=150, max_value=500, value=350)

if st.button("🎲 메뉴 추천"):
    candidates = [(m, k) for m, k in diet_menu.items() if k <= max_kcal]
    available = [(m, k) for (m, k) in candidates if m not in st.session_state.recent_menu]

    if not available:
        st.warning("추천 가능한 메뉴가 없어요. 최근 추천 내역 초기화됨.")
        st.session_state.recent_menu = []
        available = candidates

    menu, kcal = random.choice(available)
    st.success(f"✅ 추천 메뉴: **{menu}** ({kcal} kcal)")
    st.session_state.recent_menu.append(menu)
    if len(st.session_state.recent_menu) > 5:
        st.session_state.recent_menu.pop(0)

# ----------------------------
# 6. 이전 추천/체중 보기
# ----------------------------
with st.expander("📜 체중 기록 전체 보기"):
    if st.session_state.weights:
        for date, wt in st.session_state.weights:
            st.write(f"{date}: {wt}kg")
    else:
        st.write("아직 기록된 체중이 없어요.")

with st.expander("🍴 최근 추천 메뉴 보기"):
    st.write(st.session_state.recent_menu if st.session_state.recent_menu else "없음")
