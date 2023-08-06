class Employee:
    
    def __init__(self, name, salary, phoneNum):
        self.name = name
        self.salary = salary
        self.phoneNum = phoneNum
    
    def updateSalary(self,salary):
        try:
            float(salary)
        except:
            return "Exception raised: salary must be an number"       
        else:
            self.salary = salary
    
    def validPhoneNum(self, phoneNum):
        phoneNumList = phoneNum.split("-")
        if len(phoneNumList) != 3:
            return False
        elif len(phoneNumList[0]) != 3 or len(phoneNumList[1]) != 3 or len(phoneNumList[2]) != 4:
            return False
        elif not (phoneNumList[0].isdigit() and phoneNumList[1].isdigit() and phoneNumList[2].isdigit()):
            return False
        else:
            return True         
        
    def updatePhoneNum(self, phoneNum):
        try:
            if self.validPhoneNum(phoneNum):
                self.phoneNum = phoneNum
            else:
                raise(PhoneNumberFormatError(phoneNum))
                
        except PhoneNumberFormatError as pnfe:
            return "PhoneNumberFormatError: invaild phone number format, your input is " + str(pnfe.value)
        
        except: return "Exception raised: something goes wrong when updating phone number"
            
        
    def display(self):
        return "name:{}, salray:{}, phoneNum:{}".format(self.name, self.salary, self.phoneNum)
    


class PhoneNumberFormatError(Exception):
    def __init__(self, value):
        self.value = value
    