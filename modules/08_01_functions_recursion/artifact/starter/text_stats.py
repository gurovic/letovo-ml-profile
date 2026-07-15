"""Библиотека text_stats — частоты слов и простой классификатор отзывов.

Реализовать функции по artifact/PROJECT.md. Тесты: manual_tests.py
"""

import re  # нужен для tokenize


def tokenize(text: str) -> list:
    """Разбить текст на слова: lower; токены — подряд идущие буквы/цифры (regex \\w+, Unicode).

    Пример: "Hello, мир!" → ["hello", "мир"]
    """
    raise NotImplementedError


def count_words(tokens: list) -> int:
    """Число токенов."""
    raise NotImplementedError


def word_frequencies(tokens: list) -> dict:
    """Частоты слов."""
    raise NotImplementedError


def filter_tokens(tokens, min_len=3):
    """Токены длиной >= min_len."""
    raise NotImplementedError


def top_n(freq: dict, n=5) -> list:
    """Top-n (word, count) по убыванию частоты."""
    raise NotImplementedError


def count_char_recursive(s: str, ch: str) -> int:
    """Рекурсивный подсчёт символа ch в s."""
    raise NotImplementedError


def analyze_text(text: str) -> dict:
    """word_count, unique_words, top3."""
    raise NotImplementedError


def apply_pipeline(data, steps: list):
    """Последовательно применить функции."""
    raise NotImplementedError


def aggregate_frequencies(texts: list) -> dict:
    """Объединить частоты по списку текстов одного класса."""
    raise NotImplementedError


def compare_class_frequencies(texts_a: list, texts_b: list, ratio=2.0) -> dict:
    """Слова-маркеры: {word: 'positive'|'negative'} при перевесе частоты >= ratio."""
    raise NotImplementedError


def naive_classify(text: str, texts_a: list, texts_b: list) -> str:
    """'positive' / 'negative' / 'unknown' по маркерным словам; tie → 'unknown'."""
    raise NotImplementedError
