import streamlit as st

st.set_page_config(page_title="Paralympics", layout="wide")

# Row 1: two columns
# use [1,1] for equal widths or e.g. [1,3] for 1:3
left_col, right_col = st.columns([1, 3])

with left_col:
    st.subheader("Selectors")
    opts = ("Trends in number of sports, events, counties, participants",
            "Participants by gender",
            "Paralympics locations")
    select_chart = st.selectbox("Choose a chart:",
                                opts,
                                index=None,
                                placeholder="Select chart to view...")

    # Conditional rendering based on the option chosen in select_chart
    if select_chart == opts[0]:
        select_trend_type = st.selectbox("Choose the feature to display:",
                                         ["Sports", "Events", "Countries",
                                          "Participants"])

with right_col:
    st.subheader("Charts")

# Row 2: full-width (spans both columns)
st.divider()  # Added to show the separation visually, not required
full_width = st.container()

with full_width:
    st.subheader("Questions")

options = ["Winter", "Summer"]
selection = st.pills("Seasons", options, selection_mode="multi")
st.markdown(f"Your selected options: {selection}.")

with full_width:
    st.write("Answer the questions using the charts to help you.")
    with st.form("questions"):
        question_one = st.text_input("Question one?", "Enter your answer here")
        st.form_submit_button("Submit your answers")

# Inject custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    .stSelectbox label {
        color: #000000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
