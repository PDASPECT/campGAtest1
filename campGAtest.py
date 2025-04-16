import streamlit as st
import pandas as pd
from collections import defaultdict

def assign_activities(num_counselors, student_preferences):
    max_students_per_session = num_counselors * 8
    sessions = ['Session 1 (11:00 AM)', 'Session 2 (12:30 PM)', 'Session 3 (2:00 PM)']
    schedule = {session: defaultdict(list) for session in sessions}
    assigned_students = {session: set() for session in sessions}
    student_assignments = {student: [] for student in student_preferences}

    # Loop through 3 sessions
    for session in sessions:
        # Try to give each student one activity per session
        for student, preferences in student_preferences.items():
            if student in assigned_students[session]:
                continue  # already placed

            for activity in preferences:
                # Avoid duplicates and overflow
                total_in_session = sum(len(schedule[session][a]) for a in schedule[session])
                if total_in_session >= max_students_per_session:
                    break  # session full

                if student not in schedule[session][activity] and len(schedule[session][activity]) < max_students_per_session:
                    schedule[session][activity].append(student)
                    assigned_students[session].add(student)
                    student_assignments[student].append(activity)
                    break  # move to next student

    return schedule
