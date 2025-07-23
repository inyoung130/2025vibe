import streamlit as st
from PIL import Image, ImageDraw

# 페이지 설정
st.set_page_config(page_title="시향이 화장 게임", layout="centered")

st.title("💄 시향이 화장해주기 게임")

# 기본 이미지 불러오기
base = Image.open("8c2aedac-1e36-46a1-9ecc-fbcd76c510c1.png")  # 업로드된 이미지 사용
image = base.copy()
draw = ImageDraw.Draw(image)

# 색상 선택
st.sidebar.header("🎨 화장 색상 선택")

lip_color = st.sidebar.color_picker("👄 립스틱", "#FF5E78")
cheek_color = st.sidebar.color_picker("🍑 볼터치", "#FFA07A")
eye_color = st.sidebar.color_picker("👁 아이섀도우", "#9370DB")

# 버튼 클릭 시 화장 적용
if st.button("✨ 시향이 화장해줘"):
    # 대략적인 좌표, 실제 얼굴 위치에 맞게 조정 필요
    draw.ellipse((150, 300, 190, 340), fill=cheek_color)  # 왼쪽 볼
    draw.ellipse((310, 300, 350, 340), fill=cheek_color)  # 오른쪽 볼
    draw.rectangle((220, 370, 280, 385), fill=lip_color)  # 입술
    draw.rectangle((160, 230, 200, 245), fill=eye_color)  # 왼쪽 아이섀도우
    draw.rectangle((300, 230, 340, 245), fill=eye_color)  # 오른쪽 아이섀도우

    st.image(image, caption="화장한 시향이 💖", use_column_width=True)

# 다시 하기
st.button("🔄 다시 하기", on_click=st.experimental_rerun)
