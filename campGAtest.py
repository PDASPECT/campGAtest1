import streamlit as st
import pandas as pd
from collections import defaultdict

def assign_activities(num_counselors, student_preferences):
    max_students_per_session = num_counselors * 8
    sessions = ['Session 1 (11:00 AM)', 'Session 2 (12:30 PM)', 'Session 3 (2:00 PM)']
    activity_demand = defaultdict(list)

    for student, prefs in student_preferences.items():
        for rank, activity in enumerate(prefs):
            activity_demand[activity].append((rank, student))

    sorted_activities = sorted(activity_demand.items(), key=lambda x: len(x[1]), reverse=True)

    schedule = {session: defaultdict(list) for session in sessions}
    session_counts = {session: 0 for session in sessions}

    for activity, students in sorted_activities:
        students.sort()
        idx = 0
        while idx < len(students):
            for session in sessions:
                if session_counts[session] >= max_students_per_session:
                    continue
                if len(schedule[session][activity]) < max_students_per_session:
                    schedule[session][activity].append(students[idx][1])
                    session_counts[session] += 1
                    idx += 1
                if idx >= len(students):
                    break
    return schedule

st.set_page_config(page_title="Summer Camp Scheduler", layout="wide")
st.title("🏕️ campGAtest1 – Summer Camp Activity Scheduler")

num_counselors = st.sidebar.number_input("Number of Counselors", min_value=1, step=1, value=4)

uploaded_file = st.sidebar.file_uploader("Upload Student Preferences (CSV)")

st.sidebar.markdown("""
**CSV Format:**
- Column 1: Student
- Column 2–9: Rank1 to Rank8 (activities)
""")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    student_preferences = df.set_index('Student').T.to_dict(orient='list')
    schedule = assign_activities(num_counselors, student_preferences)

    st.header("📅 Daily Schedule")

    for session, activities in schedule.items():
        st.subheader(session)
        session_df = pd.DataFrame({activity: pd.Series(students) for activity, students in activities.items()})
        session_df.fillna('', inplace=True)
        st.dataframe(session_df, use_container_width=True)
