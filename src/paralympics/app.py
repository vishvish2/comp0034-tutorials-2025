import streamlit as st

from paralympics.charts import scatter_map, line_chart, bar_chart

st.set_page_config(page_title="Paralympics", layout="wide")

# Row 1: two columns
# use [1,1] for equal widths or e.g. [1,3] for 1:3
left_col, right_col = st.columns([1, 3])


# 2. Callback to clear the state of the secondary selectors when the chart
# type is changed
def clear_other_state():
    """Clear irrelevant widget state whenever the chart choice changes."""
    for key in ["trend_feature", "bar_pills"]:
        st.session_state.pop(key, None)


left_col, right_col = st.columns([1, 3])

with left_col:
    # 1. Choose chart
    st.selectbox(
        "Choose a chart:",
        ["Trends", "Participants by gender", "Paralympics locations"],
        key="chart_choice",
        index=None,
        placeholder="Select chart to view...",
        on_change=clear_other_state
    )

    # 3. Line chart → show the second selectbox
    if st.session_state.get("chart_choice") == "Trends":
        st.selectbox(
            "Choose feature:",
            ["Sports", "Events", "Countries", "Participants"],
            key="trend_feature"
        )

    # 5. Bar chart → show pills
    elif st.session_state.get("chart_choice") == "Participants by gender":
        st.pills(
            "Choose the type of Paralympics:",
            ["Winter", "Summer"],
            key="bar_pills",
            selection_mode="multi"
        )

with right_col:
    # 4. Draw a line chart after the feature is selected
    if st.session_state.get("chart_choice") == "Trends" and st.session_state.get("trend_feature"):
        feature = str.lower(st.session_state.trend_feature)
        fig = line_chart(feature)
        st.plotly_chart(fig, width="content")

    # 6. Draw one or more bar charts depending on pill selection
    if st.session_state.get("chart_choice") == "Participants by gender" and st.session_state.get(
            "bar_pills"):
        for pill in st.session_state.bar_pills:
            event_type = str.lower(pill)
            fig = bar_chart(event_type)
            st.plotly_chart(fig, width="content")

    # 7. Map chart displays once chosen
    if st.session_state.get("chart_choice") == "Paralympics locations":
        fig = scatter_map()
        st.plotly_chart(fig, width="content")

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
