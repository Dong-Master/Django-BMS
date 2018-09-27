#coding:utf-8
#@mail:879995812@qq.com

from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'addbook',Addbook.as_view(),name='addbook'),
    url(r'create_details',Create_Details.as_view(),name='create_details'),
    url(r'book_del',Book_Del.as_view(),name='book_del'),
    url(r'edit_book/(?P<book_id>\d+)/$',Edit_Book.as_view(),name='edit_book'),
]