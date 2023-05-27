from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("wiki/<str:title>", views.content, name ='entry'),
    path('search/', views.search, name ='search'),
    path("newpage/", views.new_page, name = 'new_page'), 
    path ("editpage/", views.edit_page, name = 'edit_page'),
    path("save_page/", views.save_page, name = 'save_page'),
    path("random_page/", views.random_page, name = 'random_page'),
    path("<str:old_url>", views.old_url_redirect),
    path('<str:title>/', views.content, name='entry')

]

