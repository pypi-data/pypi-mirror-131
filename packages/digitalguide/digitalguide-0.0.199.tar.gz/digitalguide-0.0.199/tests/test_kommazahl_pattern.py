from digitalguide.pattern import KOMMAZAHL_PATTERN
import pytest

@pytest.mark.parametrize("kommazahl", [
    "5,3",
    "5"
    "12356,23432"
])
def test_kommazahl_pattern_positiv(kommazahl):
    assert(KOMMAZAHL_PATTERN.search(kommazahl))

@pytest.mark.parametrize("kommazahl", [
    "7 - 12",
    "8 und 9"
])
def test_kommazahl_pattern_multiple_positiv(kommazahl):
    assert(KOMMAZAHL_PATTERN.search(kommazahl))

@pytest.mark.parametrize("kommazahl", [
    "Es sind 9 Wochen.",
    "Ich schätze 7,3 Tage"
])
def test_kommazahl_pattern_in_text_positiv(kommazahl):
    assert(KOMMAZAHL_PATTERN.search(kommazahl))

@pytest.mark.parametrize("kommazahl", [
    "a",
    "b"
])
def test_kommazahl_pattern_negativ(kommazahl):
    assert(not KOMMAZAHL_PATTERN.search(kommazahl))