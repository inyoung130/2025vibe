import streamlit as st
import random
from collections import defaultdict
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models

# ------------------ 기본 설정 ------------------ #
st.set_page_config(page_title="점심메뉴 추천기", page_icon="🍱", layout="centered")

# 메뉴 데이터
default_menus = {
    "한식": ["김치찌개", "비빔밥", "제육볶음", "된장찌개", "불고기"],
    "중식": ["짜장면",]()
