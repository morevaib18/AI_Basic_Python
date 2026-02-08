from sklearn.linear_model import LinearRegression

f = open("Data1.txt","r")
weight=[]
nopeople=[]
for data in f:
    #we will fill the list and Split the data variable as it contains two values separated in comma
    _noofpeople,_weight = data.split(",")
    nopeople.append([int(_noofpeople)])
    weight.append(float(_weight))

linerobj = LinearRegression()
#Y=Mx + C
linerobj=linerobj.fit(nopeople,weight)
print(linerobj.predict([[3]]))



