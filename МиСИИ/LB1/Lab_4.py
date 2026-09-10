def newArr(arr: list) -> list:
    return [string for string in arr if len(string) > 5 and string.islower()]

arr = ['asdasd', 'ASFASFAF', 'asd', 'ASD', 'asfasfasfa']
print(newArr(arr))