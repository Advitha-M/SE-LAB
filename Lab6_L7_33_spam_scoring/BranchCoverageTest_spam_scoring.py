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
    # Extra tests for branch coverage and boundaries
def test_short_uppercase_word_not_counted():
    assert score_message("HI", False, 0) == 0

def test_spam_word_with_punctuation_and_caps():
    assert score_message("FREE!", False, 0) == 2

def test_zero_links_adds_nothing():
    assert score_message("hello", False, 0) == 0

def test_three_links_is_the_few_links_branch():
    assert score_message("hi", False, 3) == 1

def test_known_sender_score_exactly_zero_not_negative():
    assert score_message("free", True, 0) == 0   # 2 - 3 = -1 -> 0
    assert score_message("hi", True, 3) == 0     # 1 - 3 = -2 -> 0

def test_known_sender_score_stays_positive():
    assert score_message("free free", True, 5) == 5  # 4 + 4 - 3

def test_classify_boundaries():
    assert classify(7) == "suspicious"
    assert classify(3) == "clean"
    assert classify(0) == "clean"

def test_filter_inbox_empty_list():
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}

def test_status_boundary_half_is_noisy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 1}) == "noisy"

def test_status_boundary_fifth_is_healthy():
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 4}) == "healthy"