import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

# Example tests (given)
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0

def test_low_score_is_clean():
    assert classify(1) == "clean"

# score_message
def test_spam_words_score_two_each():
    assert score_message("free cash", False, 0) == 4

def test_all_caps_long_word_scores_one():
    assert score_message("HELLO", False, 0) == 1

def test_many_links_adds_four():
    assert score_message("hi", False, 5) == 4

def test_few_links_adds_one():
    assert score_message("hi", False, 1) == 1

def test_known_sender_negative_score_floors_at_zero():
    assert score_message("hi", True, 0) == 0

def test_known_sender_reduces_score():
    assert score_message("free free free free", True, 0) == 5

# classify
def test_classify_spam():
    assert classify(8) == "spam"

def test_classify_suspicious():
    assert classify(4) == "suspicious"

# filter_inbox
def test_filter_inbox_counts():
    messages = [
        ("FREE prize cash winner", False, 5),  # 12 -> spam
        ("hello", False, 1),                    # 1  -> clean
        ("urgent URGENT!", False, 1),           # 5  -> suspicious
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}

# inbox_status
def test_status_empty():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"

def test_status_flooded():
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"

def test_status_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 3}) == "noisy"

def test_status_healthy():
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 4}) == "healthy"