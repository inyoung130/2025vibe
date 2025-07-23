import streamlit as st
from PIL import Image

st.title("💄 시향이 화장해주기 게임")

# 기본 이미지 불러오기
base = Image.open("images/face_base.png")

# 사용자 선택 UI
st.sidebar.header("💋 화장 선택")
eyebrow_option = st.sidebar.selectbox("눈썹", ["없음", "눈썹1", "눈썹2"])
lip_option = st.sidebar.selectbox("입술", ["없음", "립1", "립2"])
shadow_option = st.sidebar.selectbox("아이섀도우", ["없음", "섀도우1", "섀도우2"])
blush_option = st.sidebar.selectbox("볼터치", ["없음", "블러셔1", "블러셔2"])

# 선택된 이미지 합성
final = base.copy()

def add_layer(option, path_prefix):
    if option != "없음":
        layer = Image.open(f"images/{path_prefix}_{option[-1]}.png")
        final.paste(layer, (0, 0), layer)

add_layer(eyebrow_option, "eyebrow")
add_layer(lip_option, "lip")
add_layer(shadow_option, "shadow")
add_layer(blush_option, "blush")

# 결과 보여주기
st.image(final, caption="시향이 완성된 화장", use_column_width=True)
