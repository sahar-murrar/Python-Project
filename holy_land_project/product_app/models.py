from product_app.views import cart
from django.db import models
from django.db.models.deletion import CASCADE
from user_app.models import *
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class catimage(models.Model):
    post=models.ForeignKey(Category,default=None,on_delete=CASCADE)
    img =models.ImageField(upload_to='images/')
    def str(self):
        return self.post.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    desc = models.TextField()
    img = models.ImageField(blank=True)
    quantity= models.IntegerField()
    category = models.ForeignKey(Category, related_name="category_products", on_delete=CASCADE)
    user = models.ManyToManyField(User, through='Cart', related_name="user_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class postimage(models.Model):
    post=models.ForeignKey(Product,default=None,on_delete=CASCADE)
    img =models.ImageField(upload_to='images/')
    def str(self):
        return self.post.title


class Address(models.Model):
    country=models.CharField(max_length=255, null=True)
    state=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    street=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    # phone_number = models.CharField(max_length=255)
    address = models.ForeignKey(Address, related_name='order_address',  null=True, on_delete=CASCADE)
    product=models.ManyToManyField(Product, through='Cart', related_name="ordered_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    price = models.FloatField()
    quantity = models.IntegerField()
    user = models.ForeignKey(User, related_name="user_carts", on_delete=CASCADE)
    product= models.ForeignKey(Product, related_name="product_carts", on_delete=CASCADE)
    order = models.ForeignKey(Order, related_name="order_carts", null=True, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def get_all_categories():
    return Category.objects.all()


def get_all_products():
    return Product.objects.all()


def get_all_category_products(title):
    category=Category.objects.get(title=title)
    return category.category_products.all()


def get_reviews_for_product(productId):                                                       
    product= Product.objects.get(id=productId)
    return product.product_reviews.all()    


def get_all_cart_products(userId):
    # cart= Cart.objects.get(id= cartId) 
    user = User.objects.get(id=userId)
    user_carts_list=user.user_carts.all()  
    return user_carts_list

def get_all_user_carts(user_email):
    user = User.objects.get(email= user_email)
    all_carts = user.user_carts.all()
    return all_carts
    # carts =[]
    # for cart in all_carts:
    #     if (cart.order.id is not None):
    #         carts.push(cart)
    # return carts  

def create_order(country, state, city, street):
    return Order.objects.create(country=country, state=state, city=city, street=street)          

def create_cart(totalPrice, quantity, user, product):
    return Cart.objects.create(price=totalPrice, quantity=quantity, user=user, product=product )

def get_product_withId(productId):
    return Product.objects.get(id=productId) 

def connect_cart_withOrder(cart, orderId):
    # order=Order.objects.create()
    order= Order.objects.get(id=orderId)
    order.order_carts.add(cart)
    # cart.order_id=orderId      

def createOrder_andConect(cart):
    order=Order.objects.create()
    order.order_carts.add(cart)
    return order     

def get_user_Fistcart_orderId(user):
    all_carts=user.user_carts.all()
    return all_carts[0]

def get_cart(cartId):
    return Cart.objects.get(id=cartId)  

def remove_cart(cartId):
    cart = Cart.objects.get(id=cartId)  
    return cart.delete() 

def remove_cart_order(orderId):
    order = Order.objects.get(id=orderId)
    order.delete()
             

def create_address(country, state, city, street):
    return Address.objects.create(country=country, state=state, city=city, street=street)  

def connect_address_with_order(addressId, orderId):
    order =Order.objects.get(id=orderId)
    address= Address.objects.get(id=addressId)
    address.order_address.add(order)  
    order.address.id=addressId
    order.save()