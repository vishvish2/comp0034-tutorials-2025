import streamlit as st


st.page_config("Teacher")


def process_form() -> None:
    # Get the form values from the session state
    question_text = st.session_state.question_text
    response_text_1 = st.session_state.response_text_1
    response_text_2 = st.session_state.response_text_2
    response_text_3 = st.session_state.response_text_3
    response_text_4 = st.session_state.response_text_4
    is_correct_1 = st.session_state.is_correct_1
    is_correct_2 = st.session_state.is_correct_2
    is_correct_3 = st.session_state.is_correct_3
    is_correct_4 = st.session_state.is_correct_4


name = st.text_input("Name")

if st.button("Submit"):
    if not name.strip():
        st.error("Name is required.")
    else:
        st.success(f"Submitted: {name}")
