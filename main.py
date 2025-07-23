import streamlit as st
import random
import requests
from collections import defaultdict

# ------------------ 설정 ------------------ #
st.set_page_config(page_title="점심메뉴 추천기", page_icon="🍱", layout="centered")

# OpenWeatherMap API 키 입력
API_KEY = "여기에_당신의_API_키를_입력하세요"
CITY = "Seoul"
UNITS = "metric"

# ------------------ 초기화 ------------------ #
default_menus = {
    "한식": ["김치찌개", "비빔밥", "제육볶음", "된장찌개", "불고기"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "볶음밥"],
    "일식": ["스시", "우동", "라멘", "가츠동", "돈부리"],
    "양식": ["파스타", "스테이크", "피자", "햄버거", "샐러드"]
}

if "menus" not in st.session_state:
    st.session_state.menus = default_menus.copy()
if "votes" not in st.session_state:
    st.session_state.votes = defaultdict(int)
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ 날씨 기능 ------------------ #
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang=kr"
    try:
        res = requests.get(url)
        data = res.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["main"]
        return temp, weather
    except:
        return None, None

def weather_based_recommendation(temp, weather):
    if temp is None:
        return None
    if temp >= 28:
        return "냉면", "더운 날씨에는 시원한 냉면 어때요?"
    elif weather == "Rain":
        return "파전", "비 오는 날엔 역시 파전이죠!"
    elif temp <= 5:
        return "칼국수", "추운 날엔 따뜻한 칼국수가 딱이에요!"
    else:
        return None, None

# ------------------ UI ------------------ #
st.title("🍽️ 오늘 뭐 먹지?")

# 날씨 추천
with st.expander("🌤️ 오늘 날씨 기반 추천 메뉴"):
    temp, weather = get_weather()
    if temp is not None:
        st.markdown(f"📍 현재 서울 날씨: **{weather}**, 기온: **{temp}°C**")
        rec, comment = weather_based_recommendation(temp, weather)
        if rec:
            st.info(f"👉 {comment} 추천 메뉴는 **{rec}**!")
        else:
            st.write("☁️ 특별한 추천 조건은 없어요. 아래에서 직접 골라보세요.")
    else:
        st.error("날씨 정보를 가져올 수 없습니다. API 키를 확인해주세요.")

# 카테고리 필터
selected_categories = st.multiselect("🍱 카테고리를 선택하세요", list(st.session_state.menus.keys()))

# 메뉴 추가
with st.expander("➕ 메뉴 추가"):
    new_menu = st.text_input("메뉴 이름")
    new_category = st.selectbox("카테고리", list(st.session_state.menus.keys()))
    if st.button("메뉴 추가하기"):
        if new_menu:
            st.session_state.menus[new_category].append(new_menu)
            st.success(f"{new_menu}이(가) {new_category}에 추가되었습니다!")

# 메뉴 추천
if st.button("✅ 메뉴 추천받기"):
    if selected_categories:
        pool = sum([st.session_state.menus[cat] for cat in selected_categories], [])
    else:
        pool = sum(st.session_state.menus.values(), [])

    if pool:
        choice = random.choice(pool)
        st.subheader(f"✨ 오늘의 추천 메뉴는... **{choice}**!")
        st.session_state.history.append(choice)

        # 투표 기능
        if st.button("👍 이 메뉴 먹고 싶어요! 투표"):
            st.session_state.votes[choice] += 1
            st.success(f"{choice}에 투표했어요!")
    else:
        st.warning("추천할 메뉴가 없습니다. 메뉴를 추가하거나 카테고리를 선택해주세요.")

# 인기 메뉴 랭킹
with st.expander("🏆 인기 메뉴 투표 순위"):
    if st.session_state.votes:
        sorted_votes = sorted(st.session_state.votes.items(), key=lambda x: x[1], reverse=True)
        for i, (menu, count) in enumerate(sorted_votes, start=1):
            st.write(f"{i}. **{menu}** — {count}표")
    else:
        st.write("아직 투표된 메뉴가 없어요.")

# 추천 내역
if st.checkbox("📜 추천 내역 보기"):
    st.write(st.session_state.history[::-1])
