from django.db import models

# Create your models here.
import re
from datetime import *

class UserManager(models.Manager):
    def register(self, postData):

        #RegEx for email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #RegEx for Password
        PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d,!@#$%^&*+=]{8,}$')

        FISRT_NAME_REGEX = re.compile(r'^[a-zA-Z0-9]+$')

        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z0-9]+$')

        errors = {}

        # Validating Email
        if len(postData['email']) < 1:
            errors['email'] = 'Email is required!'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email-invalid'] = 'Invalid Email!'
        check = User.objects.filter(email=postData['email'].lower())
        if len(check) > 0:
            errors['email-inuse'] = 'Email already in use!'

        # Validating Password
        if len(postData['password']) < 1:
            errors['password'] = 'Password is required!'
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password_valid'] = 'Password must contain at least 1 number and capitalization!'

        if len(postData['password_confirm']) < 1:
            errors['password_confirm'] = 'Confirm password is required!'
        elif postData['password_confirm'] != postData['password']:
            errors['passwords_match'] = 'Password must match Confirm password!'
        

        # Validating Birthday

        if len(postData['birthday']) < 10:
            errors['birthday'] = "Please enter your birthday"
        elif len(postData['birthday']) == 10:
            input_date = datetime.strptime(postData['birthday'], '%Y-%m-%d')
            age = datetime.now().year - input_date.year
            if datetime.now().month < input_date.month or (datetime.now().month == input_date.month and datetime.now().day < input_date.day):
                age -= 1
            if age < 13:
                errors['too_young'] = "You must be at least 13 years old to register"
        
        # Validating First Name 
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        elif not FISRT_NAME_REGEX.match(postData['first_name']):
            errors["first_name"] = "First Name only conatains letter"
        
        # Validating Last Name
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 3 characters"
        elif not FISRT_NAME_REGEX.match(postData['last_name']):
            errors["last_name"] = "Last Name only conatains letter"

        return errors

# Login Validation

    def login(self, postData):
        messages = []

        if len(postData['email']) < 1:
            messages.append('Email is required!')

        if len(postData['password']) < 1:
            messages.append('Password is required!')

        return messages

class User(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    is_admin = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __repr__(self):
        return f"<User object: {self.email}>"
