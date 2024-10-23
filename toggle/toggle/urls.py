from django.contrib import admin
from django.urls import path
from . views import ToggleBulb,Listener,Temp,Power

from . models import TempratureHumidity,BulbState,power
admin.site.register(TempratureHumidity)
admin.site.register(BulbState)
admin.site.register(power)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ToggleBulb.as_view()),
    path('listener/',Listener.as_view()),
    path('temp/',Temp.as_view()),
    path('power/',Power.as_view())
]
