from django.contrib import admin
from django.urls import path, include, re_path as url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('Accounts.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]