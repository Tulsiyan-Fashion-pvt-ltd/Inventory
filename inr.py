#converting value into inr form
class inr:
    def __init__(self, price=0) -> str:
        self.price = str(price)
        self.rev_val = ''
        self.val = ''
        
    
    def formate(self):    
        i = 0
        for self.num in self.price[::-1]:
            if i == 3:
                self.rev_val +=  f",{self.num}"
            elif i%2!=0 and i>3:
                self.rev_val += f",{self.num}"
            else:
                self.rev_val += self.num
            i += 1
            
        for self.num in self.rev_val[::-1]:
            self.val += self.num
        # print(self.val)
        return '₹'+self.val
    
if __name__ == "__main__":
    price = inr(200000000).formate()
    print(price)