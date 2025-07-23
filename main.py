import streamlit as st
import json
import os
from datetime import date

# 파일 경로
DATA_FILE = "study_plan.json"

# 데이터 불러오기
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# 데이터 저장하기
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("📅 스터디 플래너")

# 입력 영역
with st.form("add_task_form"):
    task = st.text_input("공부할 내용")
    category = st.selectbox("카테고리", ["수학", "영어", "한국사", "기타"])
    due = st.date_input("마감일", value=date.today())
    submitted = st.form_submit_button("추가하기")

    if submitted and task:
        st.session_state.tasks.append({
            "task": task,
            "category": category,
            "due_date": due.strftime("%Y-%m-%d"),
            "completed": False
        })
        save_tasks(st.session_state.tasks)
        st.success("✅ 할 일이 추가되었습니다!")

st.markdown("## 📋 오늘의 공부 목록")

# 체크박스 및 삭제 버튼 처리
for i, t in enumerate(st.session_state.tasks):
    col1, col2, col3 = st.columns([5, 2, 1])
    with col1:
        checked = st.checkbox(f"{t['task']} ({t['category']}) - {t['due_date']}", value=t["completed"], key=f"chk_{i}")
        st.session_state.tasks[i]["completed"] = checked
    with col2:
        if checked:
            st.success("완료!")
    with col3:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()

# 저장
save_tasks(st.session_state.tasks)
