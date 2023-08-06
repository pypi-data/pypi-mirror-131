import product
from datetime import datetime

class Food(product.Product):
    def __init__(self, name, initStock, price, unit, expiredDate, storageEnvironment, weight = None):
        product.Product.__init__(self, name, initStock, price, unit)
        self.expiredDate = expiredDate
        self.storageEnvironment = storageEnvironment
        self.weight = weight
        
    def isExpired(self):
        return datetime.strptime(self.expiredDate,"%Y-%m-%d") < datetime.today()
        
    def calculateTotalPrice(self):
        if self.weight:
            return self.price*self.weight
        else:
            return self.price
    
    def display(self):
        return (product.Product.display(self) + " Expired Date: {}; Storage Environment: {}; Weight: {};".format(self.expiredDate,self.storageEnvironment,self.weight or "N/A"))
    