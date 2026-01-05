from __future__ import annotations

from pathlib import Path
from timeit import Timer
from typing import Dict, List, Tuple, Optional


# ---------- читання файлів ----------
def read_text_auto(path: str | Path) -> str:
    data = Path(path).read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="ignore")     # fallback


# ---------- практична версія Horspool ----------
def boyer_moore_horspool(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    shift: Dict[str, int] = {}
    for i, ch in enumerate(pattern[:-1]):
        shift[ch] = m - 1 - i

    i = 0
    last = m - 1
    while i <= n - m:
        j = last
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return i
        i += shift.get(text[i + last], m)

    return -1


# ---------- KMP ----------
def kmp_search(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    # lps (longest prefix suffix)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1


# ---------- Rabin–Karp ----------
def rabin_karp_search(
    text: str, pattern: str, base: int = 256, mod: int = 1_000_000_007
) -> int:
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    h = pow(base, m - 1, mod)

    p_hash = 0
    t_hash = 0
    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if p_hash == t_hash:
            # перевірка для уникнення колізій:
            if text[i : i + m] == pattern:
                return i

        if i < n - m:
            t_hash = (t_hash - ord(text[i]) * h) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod

    return -1


# ---------- timeit ----------
def measure(func, text: str, pat: str, number: int = 300, repeat: int = 7) -> float:
    """Повертає найкращий час ОДНОГО виклику (сек)"""
    t = Timer(lambda: func(text, pat)).repeat(repeat=repeat, number=number)
    return min(t) / number


def main():
    t1 = read_text_auto("стаття 1.txt")
    t2 = read_text_auto("стаття 2.txt")

    exist_1 = "Двійковий або логарифмічний пошук"
    exist_2 = "розгорнутий зв’язний список"
    fake = "паралельний фотонний компілятор"

    # контроль: підрядки мають/не мають бути в тексті
    assert exist_1 in t1
    assert exist_2 in t2
    assert fake not in t1 and fake not in t2

    algos = [
        ("Boyer–Moore (Horspool)", boyer_moore_horspool),
        ("Knuth–Morris–Pratt", kmp_search),
        ("Rabin–Karp", rabin_karp_search),
    ]

    tests = [
        ("Стаття 1", t1, ("існує", exist_1), ("вигаданий", fake)),
        ("Стаття 2", t2, ("існує", exist_2), ("вигаданий", fake)),
    ]

    results = []
    for text_name, text, (lab1, p1), (lab2, p2) in tests:
        for pat_label, pat in [(lab1, p1), (lab2, p2)]:
            for algo_name, func in algos:
                sec = measure(func, text, pat)
                results.append((text_name, pat_label, algo_name, sec))

    # красивий вивід
    print("Час на 1 пошук (ms), best-of-repeat")
    for text_name in ("Стаття 1", "Стаття 2"):
        for pat_label in ("існує", "вигаданий"):
            print(f"\n{text_name} / підрядок: {pat_label}")
            subset = [r for r in results if r[0] == text_name and r[1] == pat_label]
            subset.sort(key=lambda x: x[3])
            for _, _, algo_name, sec in subset:
                print(f"  {algo_name:24s}: {sec*1000:.3f} ms")

    # хто найшвидший по текстах і загалом
    def sum_time(filter_fn):
        totals = {}
        for text_name, pat_label, algo_name, sec in results:
            if filter_fn(text_name, pat_label):
                totals[algo_name] = totals.get(algo_name, 0.0) + sec
        return sorted(totals.items(), key=lambda x: x[1])

    print("\n\nНайшвидший для Стаття 1 (сума 2 підрядків):", sum_time(lambda tn, pl: tn == "Стаття 1")[0])
    print("Найшвидший для Стаття 2 (сума 2 підрядків):", sum_time(lambda tn, pl: tn == "Стаття 2")[0])
    print("Найшвидший загалом (сума всіх):", sum_time(lambda tn, pl: True)[0])


if __name__ == "__main__":
    main()
