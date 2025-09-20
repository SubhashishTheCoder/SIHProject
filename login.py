import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    with st.form("my_form",width="stretch",height="stretch",clear_on_submit=True,enter_to_submit=True):
        st.header("Login Form")
        username = st.text_input(label="Username")
        password = st.text_input(label="Password",type="password")
        submitted = st.form_submit_button("Submit",width="stretch")
        if submitted:
            st.session_state.logged_in = True
            st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

quiz = st.Page("dashboard/1_Quiz.py", title="Quiz", default=True)
pathways = st.Page("dashboard/2_Pathways.py", title="Pathways")
learning_resource = st.Page("dashboard/3_Learning_Resources.py", title="Learning Resource")


if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Dashboard": [quiz, pathways, learning_resource],
        },position="sidebar"
    )
else:
    pg = st.navigation([login_page])

pg.run()


