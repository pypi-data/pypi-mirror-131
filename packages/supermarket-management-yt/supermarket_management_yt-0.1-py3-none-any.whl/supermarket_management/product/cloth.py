import product

class Cloth(product.Product):
    def __init__(self, name, initStock, price, unit, availableSizes):
        product.Product.__init__(self, name, initStock, price, unit)
        self.availableSizes = availableSizes
        
    def addSize(self,size):
        if size not in self.availableSizes:
            self.availableSizes.append(size)
        return self.availableSizes
        
    def removeSize(self,size):
        if size in self.availableSizes:
            self.availableSizes.remove(size)
        return self.availableSizes
    
    def isAvailable(self,size):
        return (size in self.availableSizes)
    
    def display(self):
        return (product.Product.display(self) + " Available Sizes: {};".format(','.join(self.availableSizes)))