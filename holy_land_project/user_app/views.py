from django.shortcuts import render, redirect
from . import models
from product_app import models as pmodel
from django.contrib import messages
import bcrypt
from django.http import JsonResponse
from product_app.models import Category
import user_app

"""
Index function: will take the user to the (Home page)
context we passed to the render contains the all store categories.
"""
def index(request):
    all_categories=pmodel.get_all_categories()  
    # user= models.get_user(request.session['User_email'])
    context={
        'All_categories':all_categories,
        # 'user':user,
    } 
    return render(request, 'home_page.html', context)



"""
Sign in: will take the user to the Sign in page when the user clicks on the sign in click.
"""
def sign_in(request):
    print('***********************')
    return render(request, 'signIn.html') 

"""
process_user function: this will do the validation for the user if he/she is logged in/regestration. if the user is logged in the or regestired it will take the user to the Home Page if not will show the user a massege with the errors he/she commited   
"""
def process_user(request):    
    if request.method == "POST":
        if request.POST['which_form'] == 'Sign_up_form':
            all_users=models.get_all_users()
            errors = models.User.objects.registration_validator(request.POST, all_users)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                print("error while registration")    
                return redirect('/sign_in')
            else:    
                fname=request.POST['fname']
                lname=request.POST['lname']
                email=request.POST['email']
                password=request.POST['pass']
                confirmpassword= request.POST['confpass'] 
                gender= request.POST['gender']
                Bday=request.POST['birthdaydate']
                if(password == confirmpassword): #even if we didn't enter a password and hit register it will render the welcome page because both password and it's confirmation are the same (they are empty)!!
                    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                    new_user=models.create_user(fname, lname, email,Bday,gender, hashed_password)
                    request.session['Userid']= new_user.id
                    request.session['User_email']= new_user.email
                    request.session['fname']= new_user.first_name
                    request.session['lname']= new_user.last_name
                    request.session['birthdaydate']=new_user.Bdate
                    request.session['gender']=new_user.gender
                    # request.session['hashed_password'] =hashed_password
                    print("you have been registered successfully!!")
                    return redirect('/') #it is not preferable to render inside the method that check for post, we have to to redirect ot a new method and make that method to render what we want.

        elif request.POST['which_form'] == 'Login_form':
            email=request.POST['email']
            request.session['User_email']= email
            user=models.get_user(email)
            all_users=models.get_all_users()
            password=request.POST['pass']
            str_error=""
            if user !=None:
                user_password=user.password
                if bcrypt.checkpw(password.encode(), user_password.encode()):
                    str_error="True"
                else:
                    str_error="False"
            else:
                messages.error(request, "there is no account for this email")
                return redirect('/sign_in')        

            # hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            errors = models.User.objects.login_validator(request.POST,user, all_users, str_error )
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                print("error while sign in")    
                return redirect('/sign_in')
            else:    
                email=request.POST['email']
                password=request.POST['pass']
                print("you have been signed in successfully!!")
                return redirect('/')            
        return redirect('/sign_in')                  

"""
logout function: will logout from the user account and redirect the user to the Home page when the user clicks on the logout click.
"""
def logout(request):
    request.session.clear()
    return redirect('/')  

"""
autocomplete function: for search ba Ajax
render the title of categories.
"""

def autocomplete(request, str): 
    data={}
    x=Category.objects.filter(title__contains=str)
    names=[]
    for i in x:
        names.append(i.title )
        data['names'] = names
    request.session['title']=names
    print(request.session['title'])
    return JsonResponse(data,safe=False)                