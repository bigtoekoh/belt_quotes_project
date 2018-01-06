from django.conf.urls import url
from . import views

urlpatterns = [
    url('add/quote/validation$', views.addQuote),
    url(r'add_to_list/(?P<quoteId>\d+)$', views.addFavorites),
    url(r'remove_from_list/(?P<quoteId>\d+)$', views.removeFavorites),
    url(r'users/(?P<userId>\d+)$', views.userProfile),
    url(r'logOut', views.logout),
    url(r'^', views.home),
]
