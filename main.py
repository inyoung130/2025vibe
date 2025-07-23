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
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY_
