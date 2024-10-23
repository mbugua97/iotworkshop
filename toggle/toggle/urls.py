from django.contrib import admin
from django.urls import path
from . views import ToggleBulb,Listener,Temp

from . models import TempratureHumidity,BulbState
admin.site.register(TempratureHumidity)
admin.site.register(BulbState)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ToggleBulb.as_view()),
    path('listener/',Listener.as_view()),
    path('temp/',Temp.as_view())
]
