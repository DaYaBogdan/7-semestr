def dirAndHelp(mass: list) -> None:
    for i in mass:
        print(i + ':\n')
        print(str(dir(i)) + '\n')
        print(help(i))
        print('\n')
    return

arr = ['clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
dirAndHelp(arr)