import streamlit as st
from connect_data_warehouse import query_flight


@st.cache_data(ttl=600)
def load_data():
    return query_flight()


def layout():
    df = load_data()

    st.title("Technical field job ads")
    st.write(
        "This dashboard shows technical field job ads from Arbetsförmedlingen's API."
    )

    st.markdown("## Job listings data")
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    layout()