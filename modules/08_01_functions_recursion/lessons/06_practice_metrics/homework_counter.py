"""Домашнее задание к уроку 3. Найдите и исправьте 2 ошибки."""

counter = 0


def increment():
    global counter
    counter += 1
    return counter


def reset_and_count(items):
    total = 0
    for x in items:
        total = total + x
    # ошибка 1: результат не возвращается


def make_multiplier(factor=2):
    def mul(x, f=factor):
        return x * f
    return mul
