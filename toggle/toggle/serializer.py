from .models import BulbState,TempratureHumidity,power

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
class BulbStateSerializer(ModelSerializer):
    class Meta:
        model=BulbState
        fields='__all__'

class TempHumSeri(ModelSerializer):
    class Meta:
        model=TempratureHumidity
        fields='__all__'

class powerSeri(serializers.ModelSerializer):
    class Meta:
        model=power
        fields='__all__'

