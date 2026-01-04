from typing import List, Optional, Tuple

def binary_search_upper_bound(arr: List[float], x: float) -> Tuple[int, Optional[float]]:
    """
    Повертає (кількість_ітерацій, верхня_межа),
    де верхня_межа = найменший елемент у arr, який >= x.
    Якщо такого елемента немає —> повертає None.

    Вимога: arr має бути відсортований за зростанням!!!
    """
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] >= x:
            upper_bound = arr[mid]      # кандидат на відповідь
            right = mid - 1         # пробуємо знайти ще менший, але >= x
        else:
            left = mid + 1

    return iterations, upper_bound

#--------TEST--------

data = [0.5, 1.2, 1.2, 2.7, 3.14, 4.0, 10.01]

print(binary_search_upper_bound(data, 1.2))   # (ітерації, 1.2)
print(binary_search_upper_bound(data, 1.21))  # (ітерації, 2.7)
print(binary_search_upper_bound(data, 0.1))   # (ітерації, 0.5)
print(binary_search_upper_bound(data, 11.0))  # (ітерації, None)
print(binary_search_upper_bound([], 5.0))     # (0, None)

