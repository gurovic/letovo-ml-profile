"""Эталонная реализация text_stats (для проверки учителем; учащиеся работают в starter/)."""

import re


def tokenize(text: str) -> list:
    """Разбить текст на слова: lower, только буквы/цифры как токены."""
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def count_words(tokens: list) -> int:
    """Число токенов."""
    return len(tokens)


def word_frequencies(tokens: list) -> dict:
    """Частоты слов."""
    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq


def filter_tokens(tokens, min_len=3):
    """Токены длиной >= min_len."""
    return [t for t in tokens if len(t) >= min_len]


def top_n(freq: dict, n=5) -> list:
    """Top-n пар (word, count) по убыванию частоты; при равенстве — по слову."""
    items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return items[:n]


def count_char_recursive(s: str, ch: str) -> int:
    """Рекурсивный подсчёт символа ch в s."""
    if s == "":
        return 0
    head = 1 if s[0] == ch else 0
    return head + count_char_recursive(s[1:], ch)


def analyze_text(text: str) -> dict:
    """word_count, unique_words, top3 — mini-EDA одного документа."""
    tokens = tokenize(text)
    freq = word_frequencies(tokens)
    return {
        "word_count": count_words(tokens),
        "unique_words": len(set(tokens)),
        "top3": top_n(freq, 3),
    }


def apply_pipeline(data, steps: list):
    """Последовательно применить функции steps к data."""
    result = data
    for step in steps:
        result = step(result)
    return result


def aggregate_frequencies(texts: list) -> dict:
    """Суммарные частоты по списку текстов одного класса."""
    total: dict[str, int] = {}
    for text in texts:
        for word, count in word_frequencies(tokenize(text)).items():
            total[word] = total.get(word, 0) + count
    return total


def compare_class_frequencies(texts_a: list, texts_b: list, ratio=2.0) -> dict:
    """Слова-маркеры: {word: 'positive'|'negative'} при ratio× перевесе частоты."""
    freq_a = aggregate_frequencies(texts_a)
    freq_b = aggregate_frequencies(texts_b)
    markers: dict[str, str] = {}
    for word in set(freq_a) | set(freq_b):
        a = freq_a.get(word, 0)
        b = freq_b.get(word, 0)
        if b == 0 and a > 0:
            markers[word] = "positive"
        elif a == 0 and b > 0:
            markers[word] = "negative"
        elif a >= ratio * b:
            markers[word] = "positive"
        elif b >= ratio * a:
            markers[word] = "negative"
    return markers


def naive_classify(text: str, texts_a: list, texts_b: list) -> str:
    """'positive' / 'negative' / 'unknown' по сумме частот маркерных слов в text."""
    markers = compare_class_frequencies(texts_a, texts_b)
    freq = word_frequencies(tokenize(text))
    score_pos = sum(freq.get(w, 0) for w, label in markers.items() if label == "positive")
    score_neg = sum(freq.get(w, 0) for w, label in markers.items() if label == "negative")
    if score_pos > score_neg:
        return "positive"
    if score_neg > score_pos:
        return "negative"
    return "unknown"
