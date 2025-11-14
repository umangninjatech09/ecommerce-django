import random
import string

def generate_order_number():
    return "ORD" + ''.join(random.choices(string.digits, k=8))
