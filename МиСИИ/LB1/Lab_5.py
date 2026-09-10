def quickSort(unsorted: list) -> list:
    
    if len(unsorted) <= 1:
        return unsorted
    
    pivot = unsorted[0]
    
    left = [num for num in unsorted if num < pivot]
    middle = [num for num in unsorted if num == pivot]
    right = [num for num in unsorted if num > pivot]
    
    return quickSort(left) + middle + quickSort(right)

array = [10, 7, 8, 9, 1, 5]
sorted_array = quickSort(array)
print("Отсортированный массив:", sorted_array)