import streamlit as st
import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = "study_plan.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# 🧠 세션 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "timers" not in st.session_state:
    st.session_state.timers = {}  # 과제별 시작시간 저장

CATEGORIES = ["국어", "수학", "영어", "사회", "과학", "한국사", "직접 입력"]

st.title("📅 스터디 플래너 + ⏱ 타이머")

# ✅ 카테고리 선택 + 직접입력
category_choice = st.selectbox("카테고리 선택", CATEGORIES)
if category_choice == "직접 입력":
    custom_category = st.text_input("카테고리 이름 입력")
    category = custom_category.strip() if custom_category else "기타"
else:
    category = category_choice

# ✏️ 과제 추가 폼
with st.form("add_task_form"):
    task = st.text_input("공부할 내용")
    due = st.date_input("마감일", value=date.today())
    submitted = st.form_submit_button("추가하기")

    if submitted and task:
        st.session_state.tasks.append({
            "task": task,
            "category": category,
            "due_date": due.strftime("%Y-%m-%d"),
            "completed": False,
            "study_minutes": 0,
            "last_started": None,
            "last_ended": None
        })
        save_tasks(st.session_state.tasks)
        st.success("✅ 할 일이 추가되었습니다!")

# 📋 과제 목록
st.markdown("## 📝 오늘의 공부 목록")

for i, t in enumerate(st.session_state.tasks):
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        label = f"{t['task']} ({t['category']}) - {t['due_date']}"
        checked = st.checkbox(label, value=t["completed"], key=f"chk_{i}")
        st.session_state.tasks[i]["completed"] = checked

        # 누적 공부 시간 출력
        total = timedelta(minutes=t.get("study_minutes", 0))
        hours = total.seconds // 3600
        minutes = (total.seconds % 3600) // 60
        st.write(f"⏱ 누적 공부 시간: {hours}시간 {minutes}분")

        # 타이머 상태에 따라 버튼 표시
        if t["task"] not in st.session_state.timers:
            if st.button(f"▶ 시작", key=f"start_{i}"):
                st.session_state.timers[t["task"]] = datetime.now()
                st.session_state.tasks[i]["last_started"] = st.session_state.timers[t["task"]].strftime("%H:%M")
                save_tasks(st.session_state.tasks)
        else:
            if st.button(f"⏹ 종료", key=f"stop_{i}"):
                start_time = st.session_state.timers.pop(t["task"])
                duration = (datetime.now() - start_time).total_seconds() / 60
                st.session_state.tasks[i]["study_minutes"] += int(duration)
                st.session_state.tasks[i]["last_ended"] = datetime.now().strftime("%H:%M")
                save_tasks(st.session_state.tasks)

        # 시작 및 종료 시간 표시
        if t.get("last_started"):
            st.write(f"🟢 시작: {t['last_started']}")
        if t.get("last_ended"):
            st.write(f"🔴 종료: {t['last_ended']}")

    with col3:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()

save_tasks(st.session_state.tasks)
