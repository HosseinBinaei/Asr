import jdatetime
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import TimeSerializer, ElapsedSerializer, DateTrackerSerializer
from core.services import elapsed

class TimeAPIView(APIView):
    """Returns current Jalali date and time."""
    @swagger_auto_schema(
        operation_description="Get current Jalali time",
        responses={200: TimeSerializer}
    )
    def get(self, request):
        now = jdatetime.datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        data = {"time": formatted_now}

        serializer = TimeSerializer(instance=data)
        return Response(serializer.data)
    

class ElapsedAPIView(APIView):
    """Returns elapsed percentage of time for year, month, week, or day based on input key (y, m, w, d)."""
    @swagger_auto_schema(
        operation_description="Get elapsed value based on key",
        responses={200: ElapsedSerializer}
    )
    def get(self, request, pk):
        now = jdatetime.datetime.now()
        data = {'value': elapsed.get_elapsed(pk, now)}

        if data["value"] is None:
            return Response({"error": "Invalid key"}, status=400)

        serializer = ElapsedSerializer(instance=data)
        return Response(serializer.data)
    

class DateTrackerAPIView(APIView):
    """Returns elapsed time values for year, month, week, or day based on input key (y, m, w, d)."""
    @swagger_auto_schema(
        operation_description="",
        responses={200, DateTrackerSerializer}
    )
    def get(self, request, pk):
        now = jdatetime.datetime.now()

        data = {'date_tracker': elapsed.waiit(pk, now)}

        if data["date_tracker"] is None:
            return Response({"Error": "Invalid key"}, status=400)
        
        serializer = DateTrackerSerializer(instance=data)
        return Response(serializer.data)
        