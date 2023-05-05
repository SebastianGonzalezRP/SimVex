my_list = ['apple', None, 'orange', None, None, None]

for i, item in reversed(list(enumerate(my_list))):
    if item is not None:
        print(i)
        break