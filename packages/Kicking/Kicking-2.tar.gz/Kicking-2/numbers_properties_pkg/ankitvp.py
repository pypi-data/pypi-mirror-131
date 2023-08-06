class CalculateDiscount:
    
     def calculate_amount_after_discount(self, totalAmount, discount):
        discount_in_number = totalAmount * (discount / 100)
        return totalAmount - discount_in_number
 
class CalculateDiscountWithTicketCode(CalculateDiscount):
    
     def calculate_amount_after_discount(self, totalAmount, discount, ticketcode_discount):
        c = CalculateDiscount()
        normal_discount_amount = c.calculate_amount_after_discount(totalAmount, discount)
        discount_in_number = ticketcode_discount / 100
        ticketcode_discount_number = totalAmount * discount_in_number
        total_discount = ticketcode_discount_number + normal_discount_amount
        return totalAmount - total_discount
        
class CalculateDiscountForLocals(CalculateDiscount):
    
     def calculate_amount_after_discount(self, totalAmount, discount, local_discount):
        c = CalculateDiscount()
        normal_discount_amount = c.calculate_amount_after_discount(totalAmount, discount)
        discount_in_number = local_discount / 100
        local_discount_number = totalAmount * discount_in_number
        total_discount = local_discount_number + normal_discount_amount
        return totalAmount - total_discount
        


#c = CalculateDiscount()
#print(c.calculate_amount_after_discount(100, 10))