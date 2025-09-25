import  streamlit as st
from backend import get_roadmap

st.title("Roadmaps")

if "shared_data" in st.session_state:
        retrieved_data = st.session_state["shared_data"]
        options = [career_path["title"] for career_path in retrieved_data["Career Paths"]]
        option = st.selectbox(
            "Which Pathway excites you the most?",
            options=options,
        )
        retrieved_data["User Choice"] = option
        roadmap = get_roadmap(retrieved_data)
        with st.container(border=True,width="stretch"):
            st.markdown(roadmap["heading"])
            for pointers in roadmap["pointers"]:
                st.markdown(f'- {pointers}')
        with st.container(border=True,width="stretch"):
            st.markdown('Learning Resources')
            for resource in roadmap["learning_resource"]:
                st.write(f"{resource['title']} -> {resource['link']}")
        with st.container(border=True,width="stretch"):
            st.markdown('Skills to Develop')
            for skills in roadmap['skills_to_develop']:
                st.markdown(f'- {skills}')
        with st.container(border=True,width="stretch"):
            st.markdown('Scope')
            for scope_keys in roadmap['scope'].keys():
                st.text(f'{roadmap['scope'][scope_keys]}')
else:
    st.warning("No data found from Page 1. Please go back and save some data.")
