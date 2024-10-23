from django.contrib import admin
from django.urls import path
from . views import ToggleBulb,Listener,Temp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ToggleBulb.as_view()),
    path('listener/',Listener.as_view()),
    path('temp/',Temp.as_view())
]
