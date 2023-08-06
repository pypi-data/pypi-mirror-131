class Product:
    productCount = 0
    def __init__(self, name, initStock, price, unit):
        self.id = Product.productCount + 1
        self.name = name
        self.num_of_inStock = initStock
        self.price = price
        self.unit = unit
        Product.productCount = Product.productCount + 1
        
    def updatePrice(self,newPrice):
        try:
            if newPrice < 0:
                raise(NegativeValueError(newPrice))
            self.price = newPrice
            return self.price
        except NegativeValueError as nvex:
            return "NegativeValueError: The input price should be a non-negative number. Your input is:" + str(nvex.value)
        except:
            return "Exception raised: Update price failed."
        
        
    def getPrice(self):
        return self.price
    
    def stock(self,quantity):
        try:
            self.num_of_inStock = self.num_of_inStock + quantity
            return self.num_of_inStock
        except TypeError:
            return "TypeError: The input quantity should be a number."
        except: return "Exception raised: Increase the number of instock failed. The the number of instock is not changed."
            

    
    def sell(self,quantity):
        try:
            self.num_of_inStock = self.num_of_inStock - quantity
            return self.num_of_inStock
        except TypeError:
            return "TypeError: The input quantity should be a number."
        except: return "Exception raised: Decrease the number of instock failed. The the number of instock is not changed."
    
    def display(self):
        return ("Product ID: {}; Product Name: {}; In Stock: {} {}; Price: {};".format(self.id,self.name,self.num_of_inStock,self.unit,self.price))
    

class NegativeValueError(Exception):
    def __init__(self, value):
        self.value = value
    