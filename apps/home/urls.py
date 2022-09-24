# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    re_path(r'^$', views.indexiew.as_view(), name='index'),
    re_path(r'page-user/$', views.page_userview.as_view(), name='page-user'),
    re_path(r'edit-user/(?P<userid>\d+)',views.page_userview.as_view(),name='edit-user'),
    re_path(r'del-user/(?P<userid>\d+)',views.delete_userview,name='del-user'),
    re_path(r'ui-tables/$', views.ui_tablesview.as_view(), name='ui-tables' ),
    
    # qr_code
    re_path(r'qr-code/$', views.qrcodeview.as_view(), name='qr-code'),
    re_path(r'qr-code/(?P<userid>\d+)$', views.qrcodeview.as_view(), name='qr-code'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)