# data533_lab4
supermarket management system

[![Build Status](https://app.travis-ci.com/xintian927/data533_lab4.svg?token=ypzMQLtr1PH4U3TDAZnq&branch=main)](https://app.travis-ci.com/xintian927/data533_lab4)


**Group Member:** Bowen Yang, Xin Tian

This package is designed to manage employee and products in a supermarket. It includes 2 sub-packages: employee and product. The details of these 2 sub-packages would be introduced separately below.

## Employee

#### Overview

This package is used to manage employees in the supermarket such as cashier and stocker. It contains three module: employee, cashier, and stocker.


#### details

- Employee Module

  - attribute:
      - name : employee name
      - salary : employee's salary
      - phoneNum : phone number

  - method:
      - display(): display employee’s name, age, salary, and phone number.
      - updateSalary(salary): update employee’s salary
      - updatePhoneNum(phoneNum): update employee’s phone number
      
      
          
- Cashier Module: inherit employee module
 
  - attribute:
    - registerNum : represent which register the cashier is working at.
    - complaintsNum : represent how many customer complaints the cashier has received.
    
  - method:
    - updateRegisterNum(): update the register number after the cashier has been assigned to another counter.
    - addComplaint(): increase the number of complaints that the cashier has received.
    - tooManyComplaints(): return true if the cashier has received over 10 complaints from customers, false otherwise.
    - display(): display cashier’s name, age, salary, phone number, number of complaints received, and register number.
    
    
    
- Stocker Module: inherit employee module
  - attribute:
    - shelvesNum: a list containing all shelves that the stocker is responsible for.

  - method:
    - addShelf(shelf): add new shelf into the shelvesNumber list
    - removeShelf(shelf): remove shelf from the shelvesNumber list
    - display(): display stocker’s name, age, salary, phone number, and shelves Number
    
    
## Products

#### Overview

This package is used to manage product in the supermarket such as food and clothes. It contains three module: Product, Food, and Cloth.


#### details

- Product Module

  - attribute:
      - id: product ID
      - name: product name 
      - numberOfInStock: quantity of product the supermarket current have in stock
      - price: the price of product per unit
      - unit: unit of product, for example, kg, pair, and etc
  - method:
     - display(): display the information of the product
     - updatePrice(price): update the price of the product
     - getPrice(): return the price of the product per unit
     - stock(): increment the quantity when a new product is received, i.e. increase the numberOfInStock by one
     - sell(): decrement the quantity when a product is sold, i.e. decrease the numberOfInStock by one
          
- Food Module: inherit Products Module, contains all attribute and methods of product
 
  - attribute:
    - expiredDate: the expired date of the food
    - storageEnvironment; the storage environment of the food, for example, room temperature
    - weight: the weight of the food measured by the unit attribute
  - method:
    - display(): display the information of the food
    - isExpired(): check if the food is expired
    - calculateTotalPrice(): get the price of the food, it is equal to the price per unit times the weight
      
      
- Clothes Module: inherit Products Module, contains all attribute and methods of product
  - attribute:
    - availableSizes:list of sizes available for the cloth.
  - method:
    - display(): display the information of the cloth.
    - addSize(size): when a new size is available, add a new size into the availableSizes list.
    - removeSize(size): when a size is no longer available, remove a size into availableSizes list.
    - isAvailable(size): check if a given size is available.