from .models import BulbState

from rest_framework.serializers import ModelSerializer

class BulbStateSerializer(ModelSerializer):
    class Meta:
        model=BulbState
        fields='__all__'