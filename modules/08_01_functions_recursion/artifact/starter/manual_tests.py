"""Ручные тесты text_stats — 10 проверок (те же, что в solution/).

Запуск только из этой папки:
  python manual_tests.py

Соответствие тест → функция:
  test_tokenize              → tokenize
  test_count_char_recursive  → count_char_recursive
  test_word_frequencies      → word_frequencies
  test_filter_tokens         → filter_tokens
  test_top_n                 → top_n
  test_apply_pipeline        → apply_pipeline
  test_analyze_text          → analyze_text (+ опционально count_words)
  test_compare_class_frequencies → aggregate_frequencies + compare_class_frequencies
  test_naive_classify_*      → naive_classify
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from text_stats import (
    apply_pipeline,
    compare_class_frequencies,
    count_char_recursive,
    filter_tokens,
    naive_classify,
    tokenize,
    top_n,
    word_frequencies,
    analyze_text,
)
from data.module_datasets import TEXTS_NEGATIVE, TEXTS_POSITIVE


def test_tokenize():
    assert tokenize("Hello World") == ["hello", "world"]
    assert tokenize("  Mixed CASE  ") == ["mixed", "case"]


def test_count_char_recursive():
    assert count_char_recursive("banana", "a") == 3
    assert count_char_recursive("", "a") == 0


def test_word_frequencies():
    assert word_frequencies(["a", "b", "a"]) == {"a": 2, "b": 1}


def test_filter_tokens():
    assert filter_tokens(["ab", "a", "abcd"], min_len=3) == ["abcd"]


def test_top_n():
    freq = {"z": 1, "a": 3, "b": 3}
    assert top_n(freq, 2) == [("a", 3), ("b", 3)]


def test_apply_pipeline():
    pipeline = [lambda s: s.strip(), lambda s: s.split(), lambda t: [w.lower() for w in t]]
    assert apply_pipeline("  Hi There ", pipeline) == ["hi", "there"]


def test_analyze_text():
    r = analyze_text("one two two three")
    assert r["word_count"] == 4
    assert r["unique_words"] == 3
    assert r["top3"][0] == ("two", 2)


def test_compare_class_frequencies():
    markers = compare_class_frequencies(TEXTS_POSITIVE, TEXTS_NEGATIVE)
    assert isinstance(markers, dict)
    assert len(markers) >= 2
    assert markers.get("отличный") == "positive"
    assert markers.get("скучный") == "negative"


def test_naive_classify_positive():
    label = naive_classify("отличный фильм рекомендую", TEXTS_POSITIVE, TEXTS_NEGATIVE)
    assert label == "positive"


def test_naive_classify_negative():
    label = naive_classify("скучный фильм потерял время", TEXTS_POSITIVE, TEXTS_NEGATIVE)
    assert label == "negative"


TESTS = [
    test_tokenize,
    test_count_char_recursive,
    test_word_frequencies,
    test_filter_tokens,
    test_top_n,
    test_apply_pipeline,
    test_analyze_text,
    test_compare_class_frequencies,
    test_naive_classify_positive,
    test_naive_classify_negative,
]

if __name__ == "__main__":
    for fn in TESTS:
        fn()
        print("OK:", fn.__name__)
    print(f"All {len(TESTS)} manual tests passed.")
