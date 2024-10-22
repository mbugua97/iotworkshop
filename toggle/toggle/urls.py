from django.contrib import admin
from django.urls import path
from . views import ToggleBulb

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ToggleBulb.as_view())
]
