import math


def leftover_func(x) -> int:
    return int(- math.sin((x + 300_000) * 0.00001 - math.pi / 30) / (x + 200_000) * 7_500_000)
