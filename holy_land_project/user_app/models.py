from django.db import models
from django.db.models.fields.related import ManyToManyField
import re
import datetime
# from product_app.models import *
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData, all_users):
        errors = {}
        regex = re.compile(r'^[a-zA-Z]+$')
        CurrentDate = datetime.datetime.now()
        # age= str(CurrentDate)- str(postData['Bday'])
        Bdate=datetime.datetime.strptime(postData['birthdaydate'],'%Y-%m-%d')
        age= CurrentDate.year - Bdate.year
        print(age) 
        if age < 13:
                errors["age"]="Your Age should be at least 13 years old!!"
        if len(postData['fname']) <  2 :
                errors["fname"] = "First Name should be at least 2 letters"
        elif not regex.match(postData['fname']):
                errors["fname"] = "First Name should contain only letters!"     
        if len(postData['lname']) < 2: 
            errors["lname"] = "Last Name should be at least 2 letters"
        elif not regex.match(postData['lname']):
                errors["lname"] = "Last Name should contain only letters!"       
        if re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',postData['email']) is None:
            errors["email"] = "Invaild Email Address!"  
        elif re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',postData['email']) is not None:
            for user in all_users:
                        if user.email == postData['email']:
                            errors["email"] = "this email is already used by another account !!"
                            print("this email is already used by another account !!")    
        if str(postData['birthdaydate']) > str(CurrentDate) :
            errors['birthdaydate'] = "Birthday date must be a past date!!"   
        if str(postData['gender']) == "" :
            errors['gender'] = "Gender must be selected!!"       
        if len(postData["pass"]) <8:
            errors["pass"] = "Your Password should be at least 8 characters!"
        elif postData["pass"] !=postData["confpass"]:
            errors["password"] = "Your Password should be the same as the Confirmation password!"
        return errors

    def login_validator(self, postData, user, all_users, str_error):
        errors = {}  
        if re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',postData['email']) is None: 
            errors["email"] = "Invaild Email Address!"
        elif  re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',postData['email']) is not None: 
            if user not in all_users:
                            errors["email"] = "there is no account for this email!!"
                            print("there is no account for this email!!")     
        if str_error =="False":
               errors["password"] = "Wrong Password!"   
        return errors    
#the relation between the car and user is many to many because one user can rent many cars and a car can be rented by many users


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    Bdate=models.DateField(default=datetime.datetime.now())
    gender=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()


def create_user(fname, lname, email,birthday, gender, password):
    return User.objects.create(first_name=fname, last_name=lname, email=email, Bdate=birthday,gender=gender, password=password)    

def get_user(email):
    # return User.objects.filter(email=email, password=password)[0] #without [0] it will return all users with this email and password, so [0] it will select only the first user that have these email and password 
    users = User.objects.filter(email=email)
    if len(users)>0: #check if the list is not empty
        return users[0]
    return None 
def get_user_withId(userId):
    return User.objects.get(id=userId)
def get_all_users():
    return User.objects.all()
