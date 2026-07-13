"""Ручные тесты text_stats. Запуск из папки starter: python manual_tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from text_stats import (
    tokenize,
    word_frequencies,
    count_char_recursive,
    analyze_text,
    compare_class_frequencies,
    naive_classify,
)
from data.module_datasets import TEXTS_POSITIVE, TEXTS_NEGATIVE


def test_tokenize():
    assert tokenize("Hello World") == ["hello", "world"]


def test_count_char_recursive():
    assert count_char_recursive("banana", "a") == 3


def test_analyze_text_keys():
    r = analyze_text("one two two")
    assert set(r.keys()) >= {"word_count", "unique_words", "top3"}


def test_compare_class_frequencies():
    markers = compare_class_frequencies(TEXTS_POSITIVE, TEXTS_NEGATIVE)
    assert isinstance(markers, dict)
    assert len(markers) >= 1


def test_naive_classify_positive():
    label = naive_classify("отличный фильм рекомендую", TEXTS_POSITIVE, TEXTS_NEGATIVE)
    assert label in ("a", "b", "positive", "negative", "unknown")


def test_word_frequencies():
    assert word_frequencies(["a", "b", "a"]) == {"a": 2, "b": 1}


if __name__ == "__main__":
    for fn in [
        test_tokenize,
        test_count_char_recursive,
        test_analyze_text_keys,
        test_word_frequencies,
        test_compare_class_frequencies,
        test_naive_classify_positive,
    ]:
        fn()
        print("OK:", fn.__name__)
    print("All manual tests passed.")
