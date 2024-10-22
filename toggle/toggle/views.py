from . models import BulbState
from . serializer import BulbStateSerializer




from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status




from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ToggleBulb(APIView):
    def get(self,request):

        try:
            state=BulbState.objects.filter().last()
            data=BulbStateSerializer(state)
            return Response({"state":data.data},status=status.HTTP_200_OK)
        except:
            return Response({"state":None},status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        try:
            state=BulbStateSerializer(data=request.data)
            if state.is_valid():
                state.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'bulb',
                    {
                        'type': 'send_update',
                        'data': state.data
                    }
                )
                return Response({"message":state.data},status=status.HTTP_201_CREATED)
        except:
            return Response({"message":state.data},status=status.HTTP_401_UNAUTHORIZED)