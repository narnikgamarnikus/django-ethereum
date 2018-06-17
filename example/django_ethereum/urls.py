# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views

app_name = 'django_ethereum'

urlpatterns = [
    re_path(
        r'^$',
        view=views.EthereumListView.as_view(),
        name='ethereum_list'
    ),
    re_path(
        r'^~create$',
        view=views.EthereumCreateView.as_view(),
        name='ethereum_create'
    ),
    re_path(
        r'^(?P<pk>\d+)$',
        view=views.EthereumDetailView.as_view(),
        name='ethereum_detail'
    ),
]
