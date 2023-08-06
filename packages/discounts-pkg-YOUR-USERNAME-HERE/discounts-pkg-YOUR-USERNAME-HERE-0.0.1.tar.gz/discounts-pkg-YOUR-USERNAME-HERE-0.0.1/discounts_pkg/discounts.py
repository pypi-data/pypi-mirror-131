class Discount:
    def get_discount(self, totalpurchase):
          discount_per = 0
          if totalpurchase >= 3000:
                 discount_per = 50
          elif totalpurchase >=2000 and totalpurchase < 3000: 
                 discount_per = 25
          else:
                 discount_per = 0
          return discount_per
    
    
    def get_discount_newuser(self):
           discount_per = 10
           return discount_per
           
if __name__ == '__main__':
  discount = Discount()

    
    