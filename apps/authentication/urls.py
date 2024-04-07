# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import re_path
from .views import login_view, register_user, logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    re_path('login/', login_view, name="login"),
    re_path('register/', register_user, name="register"),
    re_path('logout/', logout_view, name="logout"),
    # re_path("logout/", LogoutView.as_view(), name="logout_view")
]
