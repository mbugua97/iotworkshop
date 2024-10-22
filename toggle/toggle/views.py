from .models import BulbState
from .serializer import BulbStateSerializer

from rest_framework.decorators import APIView,throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .throttling import PostRateThrottle 


class CustomUserRateThrottle(UserRateThrottle):
    rate= '100/min'
    def allow_request(self, request, view):
        if request.method == 'POST':
            return super().allow_request(request, view)
        return True  # Allow other methods (GET, etc.) without throttling


class ToggleBulb(APIView):
    throttle_classes = [CustomUserRateThrottle]
    def get(self, request):
        try:
            state = BulbState.objects.last()  # Fetch the last state
            if state is None:
                return Response({"state": None}, status=status.HTTP_404_NOT_FOUND)

            data = BulbStateSerializer(state).data  # Serialize the state
            return Response({"state": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            state = BulbStateSerializer(data=request.data)
            if state.is_valid():
                state.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'bulbstate',
                    {
                        'type': 'send_update',
                        'data': state.data
                    }
                )
                return Response({"message": state.data}, status=status.HTTP_201_CREATED)
            return Response({"message": "failed", "errors": state.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
