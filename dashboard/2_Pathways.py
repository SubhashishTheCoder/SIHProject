import  streamlit as st

st.title("Pathways")

if "shared_data" in st.session_state:
        retrieved_data = st.session_state["shared_data"]
        st.header(f"Recommended Stream -> {retrieved_data["Recommended Stream"]}")
        for career_path in retrieved_data["Career Paths"]:
            with st.container():
                st.markdown(career_path["title"])
                st.write(career_path["description"])
                st.divider()
        roadmap_button = st.button("Check and Compare Pathways",width="stretch")
        if roadmap_button:
            roadmap_page = st.Page("dashboard/3_Roadmaps.py", title="Roadmap")
            st.switch_page(roadmap_page)
else:
    st.warning("No data found from Page 1. Please go back and save some data.")