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

# ------------------ 이미지 분류 모델 ------------------ #
@st.cache_resource
def load_model():
    model = models.resnet18(pretrained=True)
    model.eval()
    return model

@st.cache_resource
def load_labels():
    # ImageNet 클래스 라벨 불러오기
    import urllib
    labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    response = urllib.request.urlopen(labels_url)
    labels = [line.decode("utf-8").strip() for line in response.readlines()]
    return labels

def predict_food(image):
    model = load_model()
    labels = load_labels()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    img = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img)
        _, predicted = outputs.max(1)
        return labels[predicted.item()]

# ------------------ UI ------------------ #
st.title("🍽️ 오늘 뭐 먹지?")

# ------------------ 이미지 기반 추천 ------------------ #
with st.expander("📷 사진으로 메뉴 추천받기"):
    uploaded_image = st.file_uploader("메뉴 사진을 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="업로드한 이미지", use_column_width=True)

        with st.spinner("이미지 분석 중..."):
            predicted_label = predict_food(image)
            st.success(f"AI가 분석한 결과: **{predicted_label}**")

            # 간단한 매핑 예시
            food_map = {
                "pizza": "피자",
                "bibimbap": "비빔밥",
                "ramen": "라멘",
                "sushi": "스시",
                "steak": "스테이크",
                "kimchi": "김치찌개",
                "hamburger": "햄버거"
            }

            for keyword, menu in food_map.items():
                if keyword in predicted_label.lower():
                    st.info(f"👉 추천 메뉴: **{menu}**")
                    break
            else:
                st.warning("⚠️ 해당 음식은 목록에 없어요. 직접 추가해보세요!")

# ------------------ 카테고리 선택 및 추천 ------------------ #
selected_categories = st.multiselect("🍱 카테고리를 선택하세요", list(st.session_state.menus.keys()))

with st.expander("➕ 메뉴 추가"):
    new_menu = st.text_input("메뉴 이름")
    new_category = st.selectbox("카테고리", list(st.session_state.menus.keys()))
    if st.button("메뉴 추가하기"):
        if new_menu:
            st.session_state.menus[new_category].append(new_menu)
            st.success(f"{new_menu}이(가) {new_category}에 추가되었습니다!")

if st.button("✅ 메뉴 추천받기"):
    if selected_categories:
        pool = sum([st.session_state.menus[cat] for cat in selected_categories], [])
    else:
        pool = sum(st.session_state.menus.values(), [])

    if pool:
        choice = random.choice(pool)
        st.subheader(f"✨ 오늘의 추천 메뉴는... **{choice}**!")
        st.session_state.history.append(choice)

        if st.button("👍 이 메뉴 먹고 싶어요! 투표"):
