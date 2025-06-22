import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
from io import BytesIO
import base64

from job_market.utils import load_data, compute_skill_counts, compute_trend, filter_data, extract_keywords

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

def main():
    st.title("Job Market Intelligence Dashboard")
    data = load_data("data/jobs.csv")

    st.sidebar.header("Filters")
    title_filter = st.sidebar.text_input("Job Title Contains")
    location_filter = st.sidebar.text_input("Location Contains")

    filtered = filter_data(data, title_filter, location_filter)
    st.write(f"Showing {len(filtered)} of {len(data)} postings")

    if st.checkbox("Show Data"):
        st.dataframe(filtered)

    skills = compute_skill_counts(filtered)
    fig1 = px.bar(skills, x="skill", y="count", title="Top Skills")
    st.plotly_chart(fig1, use_container_width=True)

    trend = compute_trend(filtered)
    fig2 = px.line(trend, x="month", y="count", title="Job Postings Over Time")
    st.plotly_chart(fig2, use_container_width=True)

    wc = WordCloud(width=800, height=400).generate(" ".join(skills["skill"]))
    st.image(wc.to_array(), caption="Skill Word Cloud")

    if st.button("Download Report"):
        csv = filtered.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="report.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.sidebar.header("Keyword Extractor")
    user_text = st.sidebar.text_area("Paste Job Description")
    if st.sidebar.button("Extract Keywords") and user_text:
        tokens = extract_keywords(user_text)
        st.sidebar.write(tokens)

if __name__ == "__main__":
    main()