from employee import Employee

class Stocker(Employee):
    
    def __init__(self, name, salary, phoneNum, shelvesNum):
        Employee.__init__(self, name, salary, phoneNum)
        self.shelvesNum = shelvesNum
              
        
    def addShelf(self,shelf):
        try:
            int(shelf)
        except:
            return "Exception raised: shelf number must be an integer"       
        else:
            self.shelvesNum.append(shelf)
            
        
    def removeShelf(self, shelf):
        self.shelvesNum.remove(shelf)
        
    def display(self):
        return Employee.display(self) + ", shelvesNum:{}".format(self.shelvesNum)
    