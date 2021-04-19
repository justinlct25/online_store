import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jsn36879!",
    database='essex_online_store'
)
cursor = db.cursor(buffered=True)


class Account:
    def __init__(self, email, password, name, phone):
        self.email = email
        self.password = password
        self.name = name
        self.phone = phone

    # add account of the website, including customer, seller and admin
    def addAccount(self):
        cursor.execute("INSERT INTO accounts (email, password, name, phone, created_at) VALUES ('{}' , '{}' , '{}' , '{}' , NOW())"
                            .format(self.email, self.password, self.name, self.phone))
        db.commit()

    # used for checking if account email and password of user loggin in are correct
    # pre-condition: varchar(255) of email and pw
    # post-condition: account_id of the successfully logged in user
    def login(email, password):
        cursor.execute("SELECT id FROM accounts WHERE email like ('{}') AND password like ('{}')".format(email, password))
        account_id = cursor.fetchall()[0][0]
        return account_id
# account1 = Account('pao@gmail.com', 'pao', 'pao', '56654098').addAccount()

# Customer class inheriting the account class   
class Customer(Account):
    def __init__(self, email, password, name, phone, address, customer_id=0):
        super().__init__(email, password, name, phone)
        self.address = address 
        self.customerId = customer_id

    # function for registering customer account and insert information into the database after init
    # eg. kristine = Customer('kristine@gmail.com', '1234', 'kristine', '97039848','Wong Tai Sin').addCustomer()
    def addCustomer(self):
        #add account info to accounts table
        Account.addAccount(self) 
        cursor.execute("SELECT MAX(id) FROM accounts")
        self.accountId = cursor.fetchall()[0][0] #account_id obtained 

        #add customer info to customers table
        cursor.execute("INSERT INTO customers (address, account_id) VALUES ('{}' , '{}')"
                            .format(self.address, self.accountId))
        cursor.execute("SELECT MAX(id) FROM customers")
        self.customerId = cursor.fetchall()[0][0]
        db.commit()

    # function for creating object of customer class after login
    # pre-condition: using the returned account_id from login function
    # post-condition: create object instance of customer class
    def getCustomerInfo(account_id):
        cursor.execute("SELECT * FROM accounts INNER JOIN customers ON accounts.id = customers.account_id WHERE accounts.id = ('{}')".format(account_id))
        info = cursor.fetchall()[0]
        return Customer(info[1], info[2], info[3], info[4],info[8], info[7])
        # (self, email, password, name, phone, address, customer_id=0):

    
    def productToBasket(self, productId, quantity):
        # get the total/remaining quantity of product being sold by the seller
        cursor.execute("SELECT quantity FROM products WHERE id = '{}'".format(productId))
        productRemainQuantity = cursor.fetchall()[0][0]
        # print(productRemainQuantity)
        # count the record of product already exists in the basket
        cursor.execute("SELECT count(*) FROM basket WHERE customer_id = '{}' AND product_id = '{}'".format(self.customerId, productId))
        targetProductCount = cursor.fetchall()[0][0]
        # check if the adding quantity of product exceed the remaining quantity of product
        if quantity<=productRemainQuantity:
            # add new record of product in the basket 
            if targetProductCount == 0:
                cursor.execute("INSERT INTO basket (customer_id, product_id, quantity, created_at) VALUES ('{}' , '{}' , '{}', NOW())"
                                    .format(self.customerId, productId, quantity, self.customerId, productId))
                db.commit()
                print("Product('{}') added to the basket".format(quantity))
            # update quantity of the product in the basket
            else:
                cursor.execute("UPDATE basket SET quantity = '{}' WHERE customer_id = '{}' AND product_id = '{}'".format(quantity, self.customerId, productId))
                db.commit()
                print("Product quantity updated to '{}'".format(quantity))
        else:
            print("Quantity out of available quantity of the product")

    def checkBasket(self):
        cursor.execute("SELECT * from basket WHERE customer_id = {}".format(self.customerId))
        return cursor.fetchall()
    
    def purchaseBasketToOrder(self):
        cursor.execute("SELECT product_id, quantity from basket WHERE customer_id = {}"
                            .format(self.customerId))
        products = cursor.fetchall()
        for product in products:
            basketProductId = product[0]
            basketProductQuantity = product[1]
            purchase = Order(basketProductId, basketProductQuantity, self.customerId).purchase()
            if purchase == 'purchase successful':
                # clear the basket of the customer
                cursor.execute("DELETE FROM basket WHERE customer_id = '{}'".format(self.customerId))
                # get the quantity of product from products table and update it
                cursor.execute("SELECT quantity FROM products WHERE id = '{}'".format(basketProductId))
                quantity = cursor.fetchall()[0][0] - basketProductQuantity
                cursor.execute("UPDATE products SET quantity = '{}' WHERE id = '{}'".format(quantity, basketProductId))
                db.commit()
        
    def checkOrders(self):
        cursor.execute("SELECT * from orders WHERE customer_id = {}".format(self.customerId))
        return cursor.fetchall()


# Customer('test@gmail.com', 'test', 'test', '56654098','Harvest Hi Garden')


class Seller(Account):
    def __init__(self, email, password, name, phone, organization_id=0, third_party=0, seller_id=0 ):
        super().__init__(email, password, name, phone)
        self.thirdParty = third_party
        self.organizationId = organization_id
        self.sellerId = seller_id

    def addSeller(self):
        #add account info to accounts table
        Account.addAccount(self) 
        cursor.execute("SELECT MAX(id) FROM accounts")
        self.accountId = cursor.fetchall()[0][0] #get the account id for sellers table

        #add seller info to sellers table
        cursor.execute("INSERT INTO sellers (account_id, third_party, organization_id) VALUES ('{}','{}' , '{}')"
                            .format(self.accountId, self.thirdParty, self.organizationId))
        cursor.execute("SELECT MAX(id) FROM sellers")
        self.sellerId = cursor.fetchall()[0][0] #get the seller id for products table
        db.commit()

    def getSellerInfo(account_id): #ok
        cursor.execute("SELECT * FROM accounts INNER JOIN sellers ON accounts.id = sellers.account_id WHERE accounts.id = ('{}')".format(account_id))
        info = cursor.fetchall()[0]
        return Seller(info[1], info[2], info[3], info[4],info[10], info[9], info[7])
        # (self, email, password, name, phone, organization_id=0, third_party=0 ,seller_id=0 )

    def addProduct(self, productName, price, genre, description, quantity): #ok
        cursor.execute("INSERT INTO products (seller_id, product_name, price, genre, description, quantity, third_party) VALUES ('{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}')"
                            .format(self.sellerId, productName, price, genre, description, quantity, self.thirdParty))
        db.commit()

    def listProducts(self): #ok
        cursor.execute("SELECT * FROM products WHERE seller_id = {}"
                            .format(self.sellerId))
        result = cursor.fetchall()
        print(result)

# Third Party Individual Seller
class ThirdPartyIndividualSeller(Seller):
    def __init__(self, email, password, name, phone, organization_id=0, third_party=1):
        super().__init__(email, password, name, phone, third_party=1)
        # print(self.account_id)
        # cursor.execute("UPDATE sellers SET third_party = 1 WHERE account_id = {}"
        #                     .format(self.account_id))
        db.commit()

# Third Party Organization Seller
class ThirdPartyAdminOrgSeller(Seller):
    def __init__(self, email, password, name, phone, organization_id=0, third_party=1) :
        super().__init__(email, password, name, phone, third_party=1)
        self.organization_id = organization_id
        # cursor.execute("UPDATE sellers SET organization_id = {} WHERE id = {}"
        #                     .format(self.organizationID, self.sellerId))
        db.commit()

class Organization:
    def __init__(self, name, email, description):
        self.name = name
        self.email = email
        self.description = description
        cursor.execute("INSERT INTO organizations (email, name, description) VALUES ('{}' , '{}' , '{}')"
                            .format(self.name, self.email, self.description))
        db.commit()

    def getOrgIdFromName(name):
        cursor.execute("SELECT id FROM organizations WHERE name = '{}'".formate(name))
        return cursor.fetchall[0][0]

# Webside Admin Seller (selling admin) (not third party seller)
class WebsiteSeller(Seller):
    def __init__(self, email, password, name, phone, third_party=0):
        super().__init__(email, password, name, phone, third_party=0)


# Website Administrator (maintenance admin)
class WebsiteMaintenanceAdmin(Account):
    def __init__(self, email, password, name, phone):
        super().__init__(email, password, name, phone)


class Order():
    def __init__(self, product_id, quantity, customer_id, delivery_method=""):
        self.productId = product_id
        self.quantity = quantity
        self.customerId = customer_id
        self.deliveryMethod = delivery_method
        cursor.execute("SELECT product_name from products WHERE id = '{}'".format(self.productId))
        self.productName = cursor.fetchall()[0][0]

    # purchase all items in the basket
    # pre-condition: order instance init from the quantity an product id of item in the basket
    # post-condition: pass to the operation of choosing delivery method 
    def purchase(self):
        payMethod = input("Select payment method for product '{}' (1 - CreditCard  2 - PayPal) : ".format(self.productName))
        if payMethod == '1': # Credit Card Method
            cursor.execute("SELECT count(*) FROM creditCardRecords WHERE customer_id = '{}'".format(self.customerId))
            hasCreditCardRecord = cursor.fetchall()[0][0]
            if hasCreditCardRecord != 0:
                # useCreditCardRecord = input("Use Credit Record? (y/n) : ")
                # if useCreditRecord == 'y':
                self.chooseDeliveryMethod() # payment successful, then choose delivery method
                # elif useCreditCardRecord == 'n':
                return 'purchase successful'
            else:
                print("Credit Card Information: ")
                cardNo = input("Card Number: ")
                cardName = input("Card Holder Name: ")
                expDate = input("Expiration Date: ")
                cardCvc = input("CVC: ")
                storeCardInfo = input("Store Credit Card Information for next transaction? (y/n) : ")
                if storeCardInfo == 'y':
                    cursor.execute("INSERT INTO creditCardRecords (customer_id, card_no, card_name, exp_date, card_cvc, created_at)"
                                    "VALUES ('{}' , '{}' , '{}' , '{}' , '{}' , NOW())"
                                    .format(self.customerId, cardNo, cardName, expDate, cardCvc))  
                    db.commit()   
                    self.chooseDeliveryMethod() # payment successful, then choose delivery method
                    return 'purchase successful'
                elif storeCardInfo == 'n':
                    self.chooseDeliveryMethod() # payment successful, then choose delivery method
                    return 'purchase successful'
        elif payMethod == '2': # PayPal Method
            cursor.execute("SELECT count(*) FROM payPalRecords WHERE customer_id = '{}'".format(self.customerId))
            hasPayPalRecord = cursor.fetchall()[0][0]
            if hasPayPalRecord !=0:
                self.chooseDeliveryMethod() # payment successful, then choose delivery method
                return 'purchase successful'
            else:
                print("PayPal Information: ")
                email = input("E-mail: ")
                password = input("Password: ")
                storePayPalInfo = input("Store PayPal Information for next transaction? (y/n) : ")
                if storePayPalInfo == 'y':
                    cursor.execute("INSERT INTO payPalRecords (customer_id, email, password, created_at)"
                                    "VALUES ('{}' , '{}' , '{}' , NOW())"
                                    .format(self.customerId, email, password))
                    db.commit()
                    self.chooseDeliveryMethod() # payment successful, then choose delivery method
                    return 'purchase successful'
                elif storePayPalInfo == 'n':
                    self.chooseDeliveryMethod() # payment successful, then choose delivery method
                    return 'purchase successful'

    # post-condition: choosing delivery method and record into database the details of each order with associated delivery method   
    def chooseDeliveryMethod(self):
        cursor.execute("SELECT product_name, third_party FROM products WHERE id = '{}'".format(self.productId))
        productInfo = cursor.fetchall()
        productName = productInfo[0][0]
        isThirdParty = productInfo[0][1]
        print(isThirdParty)
        if isThirdParty == 1:
            print("Delivery Method of third-party product '{}': Postal".format(self.productName))
            cursor.execute("INSERT INTO orders (product_id, quantity, customer_id, delivery_method, created_at)"
                                "VALUES ('{}' , '{}' , '{}' , '{}' , NOW())"
                                .format(self.productId, self.quantity, self.customerId, 'Postal'))
            db.commit()
        elif isThirdParty ==0:
            deliveryMethodId = input("Choose delivery method (1 - In-house Courier  2 - Postal : ")
            deliveryMethod = ''
            if deliveryMethodId == '1':
                deliveryMethod = 'In-house Courier'
            elif deliveryMethodId == '2':
                deliveryMethod = 'Postal'
            print("Delivery Method of third-party product '{}': '{}'".format(self.productName, deliveryMethod))
            cursor.execute("INSERT INTO orders (product_id, quantity, customer_id, delivery_method, created_at)"
                                "VALUES ('{}' , '{}' , '{}' , '{}' , NOW())"
                                .format(self.productId, self.quantity, self.customerId, deliveryMethod))
            db.commit()

def listAllProducts():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


      
# -------------tested data-------------

kristine = Customer('kristine@gmail.com', '1234', 'kristine', '97039848','Wong Tai Sin').addCustomer()

# create seller account
peter = ThirdPartyIndividualSeller('peter@gmail.com', '1234', 'peter', '59011103').addSeller()
Organization('tecky','tecky@hotmail.com','tecky powerful')
peter = ThirdPartyAdminOrgSeller('peter@gmail.com', '1234', 'peter', '59011103',2).addSeller()
# peter = WebsiteSeller('peter@gmail.com', '1234', 'peter', '59011103').addSeller()
# customer = Customer.getCustomerInfo(43)
# seller = Seller.getSellerInfo(58)
# seller = Seller.getSellerInfo(47)


seller.addProduct('gun','37.6','weapon','powerful','31')
seller.addProduct('pillow','90.6','weapon','strong','41')
seller.addProduct('myself','9999','boom','strong','51')


# seller.listProducts()
customer.productToBasket(4, 20) # productId, quantity
customer.productToBasket(6, 30)
customer.productToBasket(8, 40)

# customer.purchaseBasketToOrder()

def interface():
    userType = ''
    print("Welcome to Online Market")
    loginOrReg = input("1 - Login  2 - Register : ")
    if loginOrReg == '1': # Login
        loginType = input("1 - Customer  2 - Vendor  3 - Website Seller : ")
        email = input("E-mail: ")
        pw = input("Passward: ")
        acId = Account.login(email, pw)
        if loginType == '1':
            user = Customer.getCustomerInfo(acId)
            userType = 'customer'
        elif loginType == '2':
            user = Seller.getSellerInfo(acId)
            userType = 'Seller'
        elif loginType == '3':
            user = Seller.getSellerInfo(acId)
            userType = 'Seller'
    elif loginOrReg == '2': # Register account
        regType = input("1 - Customer  2 - Vendor  3 - Website Seller : ")
        if regType == '1':
            print("Customer Registration")
            email = input("E-mail: ")
            password = input("Password: ")
            name = input("Name: ")
            phone = input("Phone: ")
            address = input("Address: ")
            user = Customer(email, password, name, phone, address).addCustomer()
            userType = 'customer'
        elif regType == '2':
            vendorType = input("1 - Individual  2 - Organization : ")
            if vendorType == '1':
                print("Individual Vendor Registration")
                email = input("E-mail: ")
                password = input("Password: ")
                name = input("Name: ")
                phone = input("Phone: ")
                user = ThirdPartyIndividualSeller(email, password, name, phone).addSeller()
                userType = 'seller'
            elif ventorType =='2':
                org = input("1 - Existing Organization  2 - Add Organization : ")
                orgId=0
                if org == '1':
                    orgName = input("Organization Name: ")
                    orgId = Organization.getOrgIdFromName(orgName)
                elif org == '2':
                    print("Organization Registration")
                    orgName = input("Organization Name: ")
                    orgEmail = input("Organization E-mail: ")
                    orgDescription = input("Description: ")
                    Organization(orgName,orgEmail,orgDescription)
                    orgId = Organization.getOrgIdFromName(orgName)
                print("Organization Vendor Admin Registration")
                email = input("E-mail: ")
                password = input("Password: ")
                name = input("Name: ")
                phone = input("Phone: ")
                user = ThirdPartyAdminOrgSeller(email, password, name, phone, orgId)
                userType = seller
        elif regType == '3':
            print("Individual Vendor Registration")
            email = input("E-mail: ")
            password = input("Password: ")
            name = input("Name: ")
            phone = input("Phone: ")
            user = ThirdPartyIndividualSeller(email, password, name, phone).addSeller()
    else: 
        return 
    print("-------MENU-------")
    while True:
        if userType=='customer':
            action = input("1 - Purchase  2 - Check Basket  3 - Check Orders  4 - Log Out")
            if action == '1':
                allProducts = listAllProducts()
                for product in allProducts:
                    print(product)
                i=0
                while i==0:
                    buy_product_id = int(input("Add to basket (product id): "))
                    buy_product_quantity = int(input("Quantity: "))
                    user.productToBasket(buy_product_id, buy_product_quantity)
                    continue_shopping = input("Continue Shopping? (y/n): ")
                    if continue_shopping == 'n':
                        i+=1
            elif action == '2':
                allBasketItems = user.checkBasket()
                for basketItem in allBasketItems:
                    print(basketItem)
                purchase = input("Purchase Shopping Basket? (y/n): ")
                if purchase == 'y':
                    user.purchaseBasketToOrder()
            elif action == '3':
                allOrders = user.checkOrders()
                for order in allOrders:
                    print(order)
            else:
                break

        elif userType=='seller':
            action = input("1 - Check Product Status  2 - Add Product  3 - Log Out")
            if action == '1':
                allSellingProducts = user.listProducts()
                for product in allSellingProducts:
                    print(product)
            elif action == '2':
                print("Add Product")
                name = input("Product Name: ")
                price = input("Price: ")
                genre = input("Genre: ")
                description = input("Description: ")
                quantity = input("Quantity: ")
                allProducts = user.addProduct(name, price, genre, description, quantity, user.organizationId)
            else:
                break



interface()