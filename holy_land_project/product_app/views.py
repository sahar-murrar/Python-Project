from typing import ContextManager
from user_app import models
from django.shortcuts import redirect, render
from . import models

"""
Cart function: this function will bring the products that the user ordered and display them in the Cart page. 
Through the dictionary(context), the user will be able to choose all products he/she wants and then send them to the DB. 
Return: if the user's email was saved, meaning if the user was logged in in the DB. 
it will take the user to the Cart page, If not it will return the user to Regestration page. 

"""
def cart(request):
 if 'User_email' in request.session:
    user=models.get_user(request.session['User_email'])
    all_user_carts=models.get_all_user_carts(request.session['User_email'])
    all_cart_products=models.get_all_cart_products(user.id)
    totalPrice=0
    for cart in all_user_carts:
        totalPrice += cart.price
    tax= 0.05*totalPrice  
    total= totalPrice+tax +15 
    request.session['totalPrice']=totalPrice
    request.session['tax'] =tax
    request.session['total']=total

    context={
      'all_cart_products':all_cart_products,
      'all_user_carts': all_user_carts,
      'totalPrice': totalPrice,
      'tax': tax,
      'total': total,      
    }

    return render(request, 'cart.html',context) 
 return redirect('/sign_in')      


"""
Souvenirs function: will display all the souvenir products inside the Souvenirs category. And through the dictionary/(context) it will allow the user to buy any product inside this category.   
"""
def souvenirs(request):
    all_products=models.get_all_category_products('Souvenirs')
    context={
        'all_souvenirs_products': all_products,
    }
    return render(request, 'souvenirs_category.html', context)                       

"""
Food function: will display all the food products inside the Food category. And through the dictionary/(context) it will allow the user to buy any product inside this category.
"""
def food(request):
    all_products=models.get_all_category_products('Food')
    context={
        'all_food_products': all_products,
    }
    return render(request, 'food_category.html', context)  

"""
Natural_products function: will display all the products inside the Natural_products category. And through the dictionary/(context) it will allow the user to buy any product inside this category.
"""
def natural_products(request):
    all_products=models.get_all_category_products('Natural Products')
    context={
        'all_naturalProducts_products': all_products,
    }
    return render(request, 'natural_products_category.html',context)  


"""
Leather & accesorries function: will display all the products inside the Leather and accessories category. And through the dictionary/(context) it will allow the user to buy any product inside this category.
"""
def Leather_accessories(request):
    all_products=models.get_all_category_products('Leather and accessories')
    context={
        'all_Leather_accessories_products': all_products,
    }
    return render(request, 'Leather_accessories_category.html', context)     

"""
Order Function: will check if the user is logged in and if the user is inside it will render him/her into the Order page after that it will display all the 
ordered products by the user in the Order Page. if the User is not logged in this function will redirect the User to the Regestration Page.
we passed the context which contains information about order such as price, tax, shipping and the products that was ordered. 
"""
def order(request):
    if 'User_email' in request.session:
        all_user_carts=models.get_all_user_carts(request.session['User_email'])
        totalPrice=0
        for cart in all_user_carts:
            totalPrice += cart.price
        tax= 0.05*totalPrice  
        total= totalPrice+tax +15 
        request.session['totalPrice']=totalPrice
        request.session['tax'] =tax
        request.session['total']=total
        # orderId=all_user_carts[0].order.id
        if 'flag' not in request.session:
            request.session['flag']=0
        context={
            'totalPrice':request.session['totalPrice'],
            'tax': request.session['tax'],
            'total': request.session['total'],
            'all_user_carts':all_user_carts,
            'flag': request.session['flag'],
        }
        return render(request, 'order1.html',context)   
    return redirect('/sign_in')   
                   

"""
process_cart: it will check if the user is logged in, recieve data from the user and store it in the DB, it will also make the calculations for the user 
and show the total price for all the products the user has ordered. it will display all the carts that belong to one user based on a condition (if the user is logged in)
Input Id belongs to the product in cart.
"""
def process_cart(request, id):
    if request.method == "POST":
        if 'User_email' in request.session:
            quantity=request.POST['quantity'] 
            product = models.get_product_withId(id)
            user=models.get_user(request.session['User_email'])
            totalPrice= int(product.price) * int(quantity)
            # new_cart= models.create_cart(totalPrice, user, product)
            user_carts_list= models.get_all_user_carts(request.session['User_email'])
            print (len(user_carts_list))
            if len(user_carts_list) != 0:
                first_cart=models.get_user_Fistcart_orderId(user) 
                print(first_cart.id)
                # if first_cart is not None:
                orderId= first_cart.order.id
                print(orderId)
                if orderId != 0:
                    new_cart= models.create_cart(totalPrice,quantity, user, product)
                    print(orderId)
                    new_order= models.connect_cart_withOrder(new_cart, orderId)
                    return redirect('/category/cart') 
                

            else: 
                new_cart= models.create_cart(totalPrice, quantity, user, product)
                new_order= models.createOrder_andConect(new_cart)  
                return redirect('/category/cart') 
        return redirect('/sign_in') 

"""
remove cart function: it will remove a product from the cart and then redirect the user to the same page.
input id belongs to the cart we want to remove.
"""
def remove_cart(request, id):
    if request.method == "POST":
        removed_cart=models.remove_cart(id)
        all_carts= models.get_all_user_carts(request.session['User_email'])
        if len(all_carts) == 0:
            removed_cart_order= models.remove_cart_order(removed_cart.order.id)
        return redirect('/category/cart') 

"""
Check out function: will take/redirect the user to the (Order page)
"""  
def checkout(request):
    if request.method == "POST":
        return redirect('/category/order')


"""
Place order function: it will process the address information while confirming the order and redirect to the same page with prining a message that indicatede that the order was placed successfully.
"""
def place_order(request):
    if request.method == "POST":
        country= request.POST['country']
        state= request.POST['state']
        city= request.POST['city']
        street= request.POST['street']
        address= models.create_address(country, state, city, street)
        print("address created successfully")
        all_user_carts=models.get_all_user_carts(request.session['User_email'])
        orderId=all_user_carts[0].order.id
        print("orderid: ***********", orderId)
        print("address-id: ***********", address.id)
        address_id=address.id
        models.connect_address_with_order(address_id,orderId)
        request.session['flag']=1
        return redirect('/category/order')





