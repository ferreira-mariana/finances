from django.urls import path

from . import views

app_name = 'finances'
urlpatterns = [
    path('month/<int:year>/<int:month>/', views.month, name='month'),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('/', views.index, name='index')
]