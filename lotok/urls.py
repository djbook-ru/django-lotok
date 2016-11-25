from django.conf.urls import url

from lotok.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'category/(?P<name>\w+)', category, name='category'),
    url(r'product/(?P<name>\w+)', product, name='product'),
]
