list1 = [10,20,30]
list2 = ['Siv', 'Raju', 'Hari']
list3 = ['Nepal', 'India', 'USA']

listZip = zip(list1, list2, list3)

for v1, v2, v3 in listZip:
    print(v1, v2, v3)

l1, l2, l3 = zip(*listZip)
print(l1, l2, l3)

