my_list = ['apple', None, 'orange', None, None, None]
number = None


for i, item in reversed(list(enumerate(my_list))):
    if item is not None:
        number = i
        break