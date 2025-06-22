import pandas as pd
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])


def load_data(path: str) -> pd.DataFrame:
    """Load job data from a CSV file."""
    return pd.read_csv(path, parse_dates=["date_posted"])


def extract_keywords(text: str) -> list[str]:
    """Extract keywords from text using simple noun filtering."""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop]
    return tokens


def compute_skill_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Compute frequency of keywords across all job descriptions."""
    counter = Counter()
    for desc in df["description"].dropna():
        counter.update(extract_keywords(desc))
    keywords, counts = zip(*counter.most_common(20)) if counter else ([], [])
    return pd.DataFrame({"skill": keywords, "count": counts})


def compute_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Return job counts by month."""
    df = df.copy()
    df["month"] = df["date_posted"].dt.to_period("M").dt.to_timestamp()
    trend = df.groupby("month").size().reset_index(name="count")
    return trend


def filter_data(df: pd.DataFrame, title: str | None = None, location: str | None = None) -> pd.DataFrame:
    """Filter dataframe by title and location."""
    if title:
        df = df[df["job_title"].str.contains(title, case=False, na=False)]
    if location:
        df = df[df["location"].str.contains(location, case=False, na=False)]
    return df