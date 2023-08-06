from django.urls import path
from . import views

app_name = 'fav_stock'

urlpatterns = [
    path('add_n_edit_fav/', views.add_n_edit_fav, name='add_n_edit_fav'),
    path('del_fav/', views.del_fav, name='del_fav'),

    path('', views.test, name='test'),
]
