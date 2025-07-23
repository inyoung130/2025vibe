import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="시향이 화장해주기", layout="centered")

st.title("💄 시향이 화장해주기 게임")

# 기본 이미지 불러오기
base_image = Image.open("sihyang_base.png")  # 화장 전 시향이 얼굴
draw = ImageDraw.Draw(base_image)

# 화장 옵션
st.subheader("1. 립스틱 색상을 골라줘!")
lip_color = st.color_picker("립스틱", "#FF5E78")

st.subheader("2. 볼터치 색상을 골라줘!")
cheek_color = st.color_picker("볼터치", "#FFA07A")

st.subheader("3. 아이섀도우 색상을 골라줘!")
eye_color = st.color_picker("아이섀도우", "#9370DB")

if st.button("✨ 화장 완료! 시향이 보여줘"):
    # 간단한 얼굴 좌표에 색상 그리기 (예시 좌표)
    # 실제 이미지에 맞춰 조정 필요!
    draw.ellipse((130, 220, 170, 260), fill=cheek_color)  # 왼쪽 볼터치
    draw.ellipse((230, 220, 270, 260), fill=cheek_color)  # 오른쪽 볼터치

    draw.rectangle((180, 300, 220, 310), fill=lip_color)  # 립스틱 (입술)

    draw.rectangle((150, 150, 180, 160), fill=eye_color)  # 왼쪽 아이섀도우
    draw.rectangle((220, 150, 250, 160), fill=eye_color)  # 오른쪽 아이섀도우

    st.image(base_image, caption="화장한 시향이 💖", use_column_width=True)

st.markdown("---")
st.button("🔁 다시 화장하기", on_click=st.experimental_rerun)
