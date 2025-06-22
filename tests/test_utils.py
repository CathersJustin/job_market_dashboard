from job_market import utils


def test_extract_keywords():
    text = "Data Scientist needed for Python analysis"
    tokens = utils.extract_keywords(text)
    assert "data" in tokens
    assert "scientist" in tokens