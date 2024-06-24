"""Декоратор для замера времени работы программы"""

import functools
import time


def timer(iters=1):
    """Функция декоратор для замера времени работы программы"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            total = 0
            for i in range(iters):
                start = time.perf_counter()
                value = func(*args, **kwargs)
                end = time.perf_counter()
                total += end - start
            print(
                f"Среднее время выполнения(количество запусков:{iters}) {func.__name__}: {round(total/iters, 4)} сек."
            )
            return value
        return wrapper
    return decorator
