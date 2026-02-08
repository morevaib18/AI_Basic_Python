#Objectoriented Programming
class Customer:
    #Variables
    strCustomerName=""
    IntAge=10
    #Functions
    def addCustomer(self):
        print("Added Customer " + self.strCustomerName)

#Call class
custobj = Customer()
#Set Variable from class
custobj.strCustomerName="Vaibhav"
#Call function from class
custobj.addCustomer()
print(custobj.strCustomerName)