from .models import Product

def quantity_check(id, total_quantity):
    p = Product.objects.get(pk=id)

    if p.quantity>=total_quantity:
        return True
    else:
        return False

# Checks if the product exists in the database...
def product_exist(name):
    p_list = Product.objects.filter(name__exact = name)
    if len(p_list)==0:
        return False
    return True
