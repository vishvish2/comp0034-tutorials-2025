import streamlit as st
import pandas as pd
from src.data.mock_api import get_event_data
from src.utils.line_chart import line_chart


@st.cache_data
def load_data():
    """ Read the JSON structured data into a pandas DataFrame

    @st.cache_data allows the data to be cached

    Returns:
        df  pandas DataFrame with the unstructured paralympics data i.e. single table
    """
    para_data = get_event_data()
    df = pd.read_json(StringIO(para_data))
    df['start'] = pd.to_datetime(df['start'], dayfirst=True)
    df['end'] = pd.to_datetime(df['end'], dayfirst=True)
    return df

st.title("Paralympics Streamlit App")

df = load_data()

st.subheader("Table of data")
st.dataframe(df)

st.subheader("Chart")
chart = line_chart("participants", df)
st.plotly_chart(chart)

