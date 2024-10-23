from .models import BulbState,TempratureHumidity,power
from .serializer import BulbStateSerializer,TempHumSeri,powerSeri

from rest_framework.decorators import APIView,throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json,requests

Root_url='http://172.31.12.175:8200'


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


class Temp(APIView):
    throttle_classes = [CustomUserRateThrottle]
    def get(self, request):
        try:
            temphum = TempratureHumidity.objects.last()  # Fetch the last state
            if temphum is None:
                return Response({"state": None}, status=status.HTTP_404_NOT_FOUND)
            data = TempHumSeri(temphum).data  # Serialize the state
            return Response({"state": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            state = TempHumSeri(data=request.data)
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
        



class Power(APIView):
    throttle_classes = [CustomUserRateThrottle]
    def get(self,request):
        data=power.objects.last()
        dataseri=powerSeri(data)
        return Response(dataseri.data)


class Listener(APIView):
    throttle_classes = [CustomUserRateThrottle]
    def post(self, request):
            data = request.data
            print("Received data:", data)
            # Access the decoded payload directly from the incoming request data
            decoded_payload = data.get('uplink_message', {}).get('decoded_payload', {})
            if not decoded_payload:
                return Response("Decoded payload is missing", status=status.HTTP_400_BAD_REQUEST)
            # Extract values from the decoded payload
            temperature = decoded_payload.get('dhtTemperature')
            humidity = decoded_payload.get('dhtHumidity')
            pressure = decoded_payload.get('bmpPressure')
            moisture = decoded_payload.get('moisture')
            frequency = decoded_payload.get('frequency')

            # Check for missing values
            if temperature is None or humidity is None:
                return Response("Temperature or humidity data missing", status=status.HTTP_400_BAD_REQUEST)

            # Prepare data to forward
            forward_data = {
                "temprature": str(temperature),
                "humidity": str(humidity),
                "pressure": str(pressure),
                "moisture": str(moisture),
                "frequency": str(frequency)
            }
            forward_url = Root_url+ "/temp/"
            # Forward the data
            response = requests.post(forward_url, data=forward_data)
            return Response("Data forwarded successfully", status=status.HTTP_200_OK)