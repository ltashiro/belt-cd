from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validateRegistration(self, form_data):
        errors = []

        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('An email in valid email format is required.')
        
        else:
            reg_check = User.objects.filter(email = form_data['email'])
            
            if reg_check:
                errors.append('The email you are trying to create an account with has already been used.')


        if len(form_data['first_name']) < 3:
            errors.append('First Name is required.')
        
        if len(form_data['username']) <3:
            errors.append('username is required.')
        
        if len(form_data['email']) < 3:
            errors.append('Email is required.')
        
        if len(form_data['password']) < 8:
            errors.append('Invalid Password')
        
        if form_data['password'] != form_data['passwordconf']:
            errors.append('Passwords do not match.')
        
        if len(form_data['datehired']) == 0:
            errors.append('Date hired cannot be blank.')
        
        return errors

    def validateLogin(self, form_data):
        errors = []

        if len(form_data['email']) == 0:
            errors.append('Email is required.')
        
        if len(form_data['password']) == 0:
            errors.append('Password is required.') 

        return errors


    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.objects.create(
            first_name = form_data['first_name'],
            username = form_data['username'],
            email = form_data['email'],
            password = hashed_pw,
            )
        return user


class User(models.Model):
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class WishManager(models.Manager):
    def validateWish(self, form_data):
        errors = []

        if len(form_data['item']) < 3: 
            errors.append('Item must be at least 3 characters.')
        if len(form_data['item']) ==0: 
            errors.append('Item cannot be blank.')
        return errors

class Wish(models.Model):
    user = models.ForeignKey(User, related_name="wishes")
    item = models.CharField(max_length=255)
    wishers = models.ManyToManyField(User, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= WishManager()