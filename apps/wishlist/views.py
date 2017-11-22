from django.shortcuts import render, redirect, HttpResponse
from .models import User, Wish
from django.db.models import Count
from django.contrib import messages
import bcrypt
from datetime import datetime
 
def dashboard(request):
    if 'user_id' in request.session:
        user = currentUser(request)
        wishes = Wish.objects.all()
        my_wishes = user.items.all()
        wishes = Wish.objects.exclude(id__in=my_wishes)
        context = {
            "user": user,
            'wishes': wishes,
            'my_wishes': my_wishes,
        }
    return render(request, 'wishlist/dashboard.html', context)


def addItem(request):
# this is for a user to add a new item to the database
    if 'user_id' in request.session:
        user = currentUser(request)
        context = {
        "user": user,
        }
    return render(request, 'wishlist/addItem.html', context)


def submitItem(request):
    if request.method == 'POST':
        errors = Wish.objects.validateWish(request.POST)

        if not errors:
            user = currentUser(request)
            wish = Wish.objects.create(item=request.POST['item'], user=user)
            user.items.add(wish)
            return redirect('/dashboard')

        for error in errors:
            messages.error(request, error)
        return redirect('/addItem')

    return redirect('/dashboard')


def addWish(request, id):
# this is to add another user's item/wish to my wish list
    if 'user_id' in request.session:
        user = currentUser(request)
        wish = Wish.objects.get(id=id)
        wish.wishers.add(user)
    return redirect('/dashboard')


def removeWish(request, id):
# this is to remove another user's item/wish from my wish list
    if 'user_id' in request.session:
        user = currentUser(request)
        wish = Wish.objects.get(id=id)
        wish.wishers.remove(user)
    return redirect('/dashboard')


def item(request, id):
    if 'user_id' in request.session:
        user = currentUser(request)
        context = {
        'user': user,
        'wish': Wish.objects.get(id=id) 
        }
    return render(request, 'wishlist/item.html', context)

def index(request):
    return render(request, 'wishlist/index.html')


def currentUser(request): 
    user = User.objects.get(id=request.session['user_id'])
    return user


def register(request):
    if request.method == 'POST':
        errors = User.objects.validateRegistration(request.POST)
        if not errors:
            user = User.objects.createUser(request.POST)
            request.session['user_id'] = user.id
            return redirect('/dashboard')


        for error in errors:
            messages.error(request, error)
        print errors
    return redirect('/')


def login(request):
    errors = User.objects.validateLogin(request.POST)
    if len(errors):
      for tag, error in errors.iteritems():
        messages.error(request, error, extra_tags=tag)
      return redirect('/')
    else:
      b = User.objects.get(email = req.POST['email'])
      req.session['id'] = b.id
      return redirect('/dashboard')


def delete(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()
    return redirect('/dashboard')

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')
    return redirect('/')