from digitalguide.pattern import JAHRESZAHL_PATTERN
import pytest

@pytest.mark.parametrize("jahreszahl", [
    "1995",
    "1650",
    "650"
])
def test_emoji_pattern_positive(jahreszahl):
    assert(JAHRESZAHL_PATTERN.search(jahreszahl))

@pytest.mark.parametrize("jahreszahl", [
    "1712 1851",
    "1712 oder 1851"
])
def test_emoji_pattern_multiple_positive(jahreszahl):
    assert(JAHRESZAHL_PATTERN.search(jahreszahl))

@pytest.mark.parametrize("jahreszahl", [
    "Es war im Jahr 1750."
    "Ich denke, es war 1927."
    "1743 war das Jahr."
])
def test_emoji_pattern_in_text_negative(jahreszahl):
    assert(JAHRESZAHL_PATTERN.search(jahreszahl))

@pytest.mark.parametrize("jahreszahl", [
    "Dies ist keine Jahreszahl.",
    "Dies ist auch keine Jahreszahl."
])
def test_emoji_pattern_negative(jahreszahl):
    assert(not JAHRESZAHL_PATTERN.search(jahreszahl))