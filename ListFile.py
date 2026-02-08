list1 = ['Vaibhav', 'Siva', 'Sada', 'Nikhil']
print(type(list1))
print(list1)
print(list1[0])
print(list1[1])
print(list1[-1])
print(list1[1:3])
print(list1[-4:-1])

for temp in list1:
    print(temp)

if 'Vaibhav1' in list1:
    print('found')
else:
    print('not found')
