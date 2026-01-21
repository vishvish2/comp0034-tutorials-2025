import streamlit as st

st.set_page_config(page_title="Paralympics", layout="wide")

# Row 1: two columns
# use [1,1] for equal widths or e.g. [1,3] for 1:3
left_col, right_col = st.columns([1, 3])

with left_col:
    st.subheader("Selectors")

with right_col:
    st.subheader("Charts")

# Row 2: full-width (spans both columns)
st.divider()  # Added to show the separation visually, not required
full_width = st.container()

with full_width:
    st.subheader("Questions")
    st.write("Answer the questions using the charts to help you.")

select_chart = st.selectbox("Choose a chart:",
                            ("Trends in number of sports, events, counties, \
                             participants",
                             "Participants by gender",
                             "Paralympics locations"),
                            index=None,
                            placeholder="Select chart to view..."
                            )
