from typing import Any, Dict, List
import requests
import streamlit as st

from paralympics.charts import scatter_map, line_chart, bar_chart

API_BASE = "http://127.0.0.1:8000"  # REST API default URL
TIMEOUT = 5  # seconds

st.set_page_config(page_title="Paralympics Dashboard", layout="wide")

# Row 1: two columns
# use [1,1] for equal widths or e.g. [1,3] for 1:3
left_col, right_col = st.columns([1, 3])


# 2. Callback to clear the state of the secondary selectors when the chart
# type is changed
def clear_other_state():
    """Clear irrelevant widget state whenever the chart choice changes."""
    for key in ["trend_feature", "bar_pills"]:
        st.session_state.pop(key, None)


# Helper functions for interacting with the REST API

def _get(url: str, **kwargs) -> requests.Response:
    """HTTP GET with a uniform timeout and error handling."""
    try:
        resp = requests.get(url, timeout=TIMEOUT, **kwargs)
        resp.raise_for_status()
        return resp
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed for {url}: {e}") from e


@st.cache_data(show_spinner=False)
def count_questions() -> int:
    """Return the number of questions available."""
    resp = _get(f"{API_BASE}/question")
    data = resp.json()
    return len(data)


@st.cache_data(show_spinner=False)
def get_question(qid: int) -> Dict[str, Any]:
    """Return the question object by ID."""
    resp = _get(f"{API_BASE}/question/{qid}")
    return resp.json()


@st.cache_data(show_spinner=False)
def get_responses(qid: int) -> List[Dict[str, Any]]:
    """Return the responses for a given question ID."""
    resp = _get(f"{API_BASE}/response/search", params={"question_id": qid})
    return resp.json()


def render_question_block():
    if "q_index" not in st.session_state:
        st.session_state.q_index = 1

    q_index = st.session_state.q_index

    # Fetch total count
    num_q = count_questions()

    # If past the last question, show completion and exit
    if q_index > num_q:
        st.success("Questions complete, well done!")
        return

    # Fetch the current question + its responses
    q = get_question(q_index)
    responses = get_responses(q_index)

    # Build radio options as label -> id map
    label_to_id = {
        r.get("response_text", ""): r.get("id") for r in responses if
        r.get("response_text", "")
                   }

    with st.form(key="quiz_form", clear_on_submit=False):
        st.write(q.get("question_text", ""))
        selected_label = st.radio(
            "Select one answer:",
            options=list(label_to_id.keys()),
            index=None,
        )
        submitted = st.form_submit_button("Submit answer")

    # Handle submission
    if submitted:
        if not selected_label:
            st.info("Please select an answer.")
            return

        selected_id = str(label_to_id[selected_label])

        # Find the selected response to inspect correctness
        selected_obj = next(
            (r for r in responses if str(r.get("id")) == selected_id),
            None,
        )

        if selected_obj and selected_obj.get("is_correct"):
            # Advance or finish
            if q_index >= num_q:
                st.session_state.q_index = num_q + 1
                st.success("Questions complete, well done!")
            else:
                st.session_state.q_index = q_index + 1
                # Using rerun ensures the next question renders cleanly
                st.rerun()
        else:
            st.info("Please try again!")


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
    if st.session_state.get("chart_choice") == "Trends"\
       and st.session_state.get("trend_feature"):
        feature = str.lower(st.session_state.trend_feature)
        fig = line_chart(feature)
        st.plotly_chart(fig, width="content")

    # 6. Draw one or more bar charts depending on pill selection
    if st.session_state.get("chart_choice") == "Participants by gender"\
       and st.session_state.get(
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


options = ["Winter", "Summer"]
selection = st.pills("Seasons", options, selection_mode="multi")
st.markdown(f"Your selected options: {selection}.")

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

# Questions
st.header("Questions")
question_container = st.container()
with question_container:
    render_question_block()
