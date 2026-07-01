import jdatetime
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import TimeSerializer, ElapsedSerializer
from core.services.elapsed import get_elapsed

class TimeAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get current Jalali time",
        responses={200: TimeSerializer}
    )
    def get(self, request):
        now = jdatetime.datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        data = {"time": formatted_now}

        #Method 1:
        serializer = TimeSerializer(instance=data)
        return Response(serializer.data)
        
        # Method 2:
        # return Response(data)
    

class ElapsedAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get elapsed value based on key",
        responses={200: ElapsedSerializer}
    )
    def get(self, request, pk):

        now = jdatetime.datetime.now()
        data = {'value': get_elapsed(pk, now)}

        if data["value"] is None:
            return Response({"error": "Invalid key"}, status=400)

        serializer = ElapsedSerializer(instance=data)
        return Response(serializer.data)