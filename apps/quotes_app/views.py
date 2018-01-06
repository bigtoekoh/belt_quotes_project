from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import Quote
from ..login_app.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    if "user" not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session["user"])
    context = {
        "user" : user,
        "quotes" : Quote.objects.all().exclude(favoritedUser = user.id),
        "quotesFavorited" : Quote.objects.filter(favoritedUser = user.id)
        }
    return render(request, 'quotes_app/home.html', context)

def addQuote(request):
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    response = Quote.objects.quote_validator(request.POST, userId)
    for val in response["errors"]:
        messages.error(request, val, extra_tags="Login")
        return redirect('/quotes_app')
    else:
        return redirect('/quotes_app')

def addFavorites(request, quoteId):
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    Quote.objects.add_to_favorites(userId, quoteId)
    return redirect('/quotes_app')

def removeFavorites(request, quoteId):
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    user = User.objects.get(id = userId)
    quote = Quote.objects.get(id=quoteId)
    userPosting = User.objects.get(id=quote.userPosting_id)
    newQuote = Quote.objects.create(author = quote.author, message = quote.message, userPosting = userPosting)
    allFavoritedUsers = User.objects.filter(id=quote.userPosting_id)
    user.favorite_quotes.get(id = quoteId).delete()
    userDeleting = userId
    print allFavoritedUsers
    for userAdding in allFavoritedUsers:
        Quote.objects.add_to_favorites_rewind(userAdding.id, newQuote.id, userDeleting)
    return redirect('/quotes_app')

def userProfile(request, userId):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id = userId),
        "quotes" : Quote.objects.filter(userPosting_id = userId)
        }
    return render(request, 'quotes_app/user.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
