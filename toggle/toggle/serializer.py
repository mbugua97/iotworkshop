from .models import BulbState,TempratureHumidity

from rest_framework.serializers import ModelSerializer

class BulbStateSerializer(ModelSerializer):
    class Meta:
        model=BulbState
        fields='__all__'

class TempHumSeri(ModelSerializer):
    class Meta:
        model=TempratureHumidity
        fields='__all__'