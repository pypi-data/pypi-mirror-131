class calcart:
    
    def __init__(self, list):
        self.list = []
        
    #Function to add the price when a item is added is to the cart
    def add_item_amount(self, cart):
        total = 0
        null = 0
        if cart != null:
            for item in self.list:
                name, price = item # or price = item[1]
                total = total + price
        else:
            print("Cart is Empty")
    
    #function to substrate the price when a item is removed for the cart
    def remove_item_amount(self,cart):
        total = 0
        null = 0
        if cart == null:
            
            print("The Cart is already empty")
        else:
            for item in self.list:
                price = item
                total = total - price
                

                
    if __name__ == '__main__':
        cal = calcart()
        cal.add_item_amount(50)
        cal.remove_item_amount(30)