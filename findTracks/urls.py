from django.urls import path

from . import views

urlpatterns = [
    path('/<str:genre>', views.spotifySearch, name='spotifySearch'), #for json result
    path('', views.mainPage, name='main'), #for user interface
]