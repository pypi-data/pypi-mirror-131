from employee import Employee

class Cashier(Employee):
    
    def __init__(self, name, salary, phoneNum, registerNum, complaintsNum):
        Employee.__init__(self, name, salary, phoneNum)
        self.registerNum = registerNum
        self.complaintsNum = complaintsNum
        
    def updateRegisterNum(self, registerNum):
        self.registerNum = registerNum
    
    def addComplaint(self):
        self.complaintsNum += 1
    
    def tooManyComplaints(self):
        return self.complaintsNum > 10
    
    def display(self):
        return Employee.display(self) + ", registerNum:{}, complaintsNum:{}".format(self.registerNum, self.complaintsNum)
    
    
            