from digitalguide.pattern import EMOJI_PATTERN
import pytest

@pytest.mark.parametrize("emoji", [
    "🏗️",
    "📚"
])
def test_emoji_pattern_positive(emoji):
    assert(EMOJI_PATTERN.search(emoji))

@pytest.mark.parametrize("emoji", [
    "🏗️📚",
    "📚📚"
])
def test_emoji_pattern_multiple_positive(emoji):
    assert(EMOJI_PATTERN.search(emoji))

@pytest.mark.parametrize("emoji", [
    "text🏗️text📚text",
    "text📚text📚text"
])
def test_emoji_pattern_in_text_negative(emoji):
    assert(EMOJI_PATTERN.search(emoji))

@pytest.mark.parametrize("emoji", [
    "a",
    "b"
])
def test_emoji_pattern_negative(emoji):
    assert(not EMOJI_PATTERN.search(emoji))