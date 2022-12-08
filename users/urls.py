from django.urls import path,include
from . import views

urlpatterns = [
  path('', views.login_user, name="login"),
  path('logout', views.logout_user, name="logout"),
  path('<str:room>/', views.room, name="room"),
  path('getMessages/<str:room>/', views.getMessages, name="getMessages"),
  path('send', views.send, name="send"),
  path('checkview', views.checkview, name="checkview")
]