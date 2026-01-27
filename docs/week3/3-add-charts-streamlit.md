# 3. Adding charts to the Streamlit app

## Setup

Ensure that you have plotly and the streamlit charts dependencies installed:

`pip install plotly`

`pip install streamlit[charts]` (on Mac you may need to use `pip install streamlit\[charts]`)

## References

You may need to refer to the following for more information.

- [State](https://docs.streamlit.io/develop/concepts/architecture/session-state)
- [Widget behaviour, e.g. select](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior)
- [Plotly charts in Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)

## Introduction

Last week you created the layout and added the dropdowns and checkboxes to select options for the
charts.

This activity implements the functionality that creates the charts when choices are made in the
selectors.

The desired behaviour is:

1. Select a chart from the "choose a chart" selectbox
2. Any time the choice of chart is changed, clear any further selectors that are not needed, and
   clear any previous charts
3. If the line chart is chosen, display a second selectbox to let you choose the feature for the
   chart.
4. Once a feature is selected, display the line chart
5. If the bar chart is chosen, display the pills to let winter/summer be chosen
6. Once a pill is selected, display one or more bar charts depending on the choice
7. If the map is chosen, display the chart(s)

## Displaying a plotly chart in streamlit

To render
a [Plotly chart in Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)
use `st.plotly_chart()`.

Create a plotly figure using the functions defined in the charts module.

Add this figure to the streamlit layout using `st.plotly_chart()`

For example:

```python
from paralympics.charts import scatter_map

fig = scatter_map()
st.plotly_chart(fig, width="content")
```

Try adding the chart to your streamlit app from last week to check that the chart displays.

## State

Streamlit defines access to an app in a browser tab as a **session**. For each browser tab that
connects to the Streamlit server, a new session is created. Streamlit reruns your script from top to
bottom every time you interact with your app. Each rerun takes place in a blank slate: no variables
are shared between runs.

**Session State** is a way to share variables between reruns, for each user session. In addition to
the
ability to store and persist state, Streamlit also exposes the ability to manipulate state using
**Callbacks**.

The callbacks let you run specific code only when a widget changes or a button is pressed,
rather than on every script rerun. They help you control flow, update `st.session_state` safely, and
co-ordinate multiple widgets.

If a single interaction affects several derived values, update them together in a callback to keep
the state consistent.

In this example, we want to make a choice of chart and keep that choice while subsequent selectors
are made available.

To achieve this you will use `st.session_state` with an `on_change` callback.

Following the logic in the introduction, the code can be implemented as follows:

1. Modify the first selectbox to add an id (`key=`) and the function to call when a choice is
   selected (`on_change=`), e.g.

    ```python
    select_chart = st.selectbox(
        "Choose a chart:",
        ["Line", "Bar", "Map"],
        key="chart_choice",
        on_change=clear_other_state
    )
    ```
2. Define a callback that clears other selectors from the state. Whenever the chart choice changes,
   remove the saved choice for the other selectors.

    ```python
    def clear_other_state():
        st.session_state.pop("trend_feature", None)
        st.session_state.pop("bar_pills", None)
    ```

3. Show the second selectbox only if "Line" is chosen:

    ```python
    if st.session_state.chart_choice == "Line":
        st.selectbox(
            "Choose trend feature:",
            ["Sports", "Events", "Countries", "Participants"],
            key="trend_feature"
        )
    ```

4. Render the chart once a feature is chosen:

    ```python
    if "trend_feature" in st.session_state and st.session_state.get("trend_feature"):
        feature = str.lower(st.session_state.trend_feature)
        fig = line_chart(feature)
        st.plotly_chart(fig, width="content")
    ```

5. Show the pills if a 'Bar' is chosen:

    ```python
    elif st.session_state.chart_choice == "Bar":
    st.pills(
        "Choose season:",
        ["Winter", "Summer"],
        key="bar_pills",
        selection_mode="multi"
    )
    ```

6. Render the bar charts

    ```python
    if st.session_state.get("chart_choice") == "Participants by gender" and st.session_state.get(
            "bar_pills"):
        for pill in st.session_state.bar_pills:
            event_type = str.lower(pill)
            fig = bar_chart(event_type)
            st.plotly_chart(fig, width="content")
    ```

7. If the map is chosen, display the map

    ```python
    if st.session_state.get("chart_choice") == "Participants by gender" and st.session_state.get(
            "bar_pills"):
        for pill in st.session_state.bar_pills:
            event_type = str.lower(pill)
            fig = bar_chart(event_type)
            st.plotly_chart(fig, width="content")
    ```

Putting this all together in the two columns gives you:

```python
# 2. Callback to clear the state of the secondary selectors when the chart type is changed
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
```

## App at the end of week 3

You should now have an app where the dropdowns and checkboxes work and display the selected
charts.

Next week will add the question/answer feature to the app.

## (Optional) Caching data

If your data set is large, you may benefit from caching the data.

Read the [Streamlit guidance](https://docs.streamlit.io/develop/concepts/architecture/caching) for
how and when to use this.

[Next activity](4-end.md)
