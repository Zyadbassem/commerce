from django.urls import path
from . import views
urlpatterns = [
    path("sign/",views.sign, name="sign"),
    path("register/", views.register, name="register"),
    path('', views.home, name="home"),
    path('logout/', views.logout, name="logout"),
    path('add/', views.addItems, name='addItems'),
    path('<int:clickedItemTitle>', views.itemPage, name='itemPage'),
    path('type/<str:typeClicked>', views.types, name="types" ),
    path('end/<str:itemToEndBid>', views.bidEnder, name="bidEnder"),
    path('watchlist/', views.watchlist, name="watchlist"),
    path('addtowatchlist/<int:itemToAdd>', views.watchlistAdder, name="watchlistAdder"),
    path('removefromwatchlist/<int:itemToRemove>', views.watchlistRemover, name="watchlistRemover"),
]