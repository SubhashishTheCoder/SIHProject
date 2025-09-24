import  streamlit as st
import json

st.set_page_config(page_title="Career Guidance Quiz", page_icon="🎓")

st.title("🎓 Career Guidance Quiz")
st.write("Answer the following questions to find out which stream suits you best!")

with open('questions.json',encoding="utf8") as file:
    questions = json.load(file)

for question in questions:
    a = [question['options'][i] for i in question['options'].keys()]
    st.radio(question['question'],a, key=f"{question['question']}")

btn_recommend = st.button("Check For Recommendation")
user_selection= []
if btn_recommend:
    for question in questions:
        user_choice = f"{question['question']} -> {st.session_state[question['question']]}"
        user_selection.append(user_choice)
    print(user_selection)