from models.nodes.node import Node

def split_list(lst, n):
    quotient, remainder = divmod(len(lst), n)
    parts = []
    index = 0
    for i in range(n):
        if i < remainder:
            size = quotient + 1
        else:
            size = quotient
        parts.append(lst[index:index + size])
        index += size
    return parts

lista =[]

for i in range(13):
    lista.append(Node())


print(len(lista))

parts = split_list(lista,3)

for item in parts:
    print (item,'\n')

print(parts)