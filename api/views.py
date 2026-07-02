from core.utils import jalali_now
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import TimeSerializer, ElapsedSerializer
from core.services import elapsed

class TimeAPIView(APIView):
    """Returns current Jalali date and time."""
    @swagger_auto_schema(
        operation_description="Get current Jalali time",
        responses={200: TimeSerializer}
    )
    def get(self, request):
        now = jalali_now()
        data = {
            'now': {},
        }
        data['now']['date'] = now.strftime("%Y/%m/%d")
        data['now']['time'] = now.strftime("%H:%M")

        serializer = TimeSerializer(instance=data)
        return Response(serializer.data)
    

class ElapsedAPIView(APIView):
    """Returns elapsed percentage of time for year, month, week, or day based on input key (y, m, w, d)."""
    @swagger_auto_schema(
        operation_description="Get elapsed value based on key",
        responses={200: ElapsedSerializer}
    )
    def get(self, request, pk=None):
        now = jalali_now()
        data = {
            'now': {},
            'elapsed': {
                'value': None,
                'percent': None
            },
        }

        data['now']['date'] = now.strftime("%Y/%m/%d")
        data['now']['time'] = now.strftime("%H:%M")

        if pk is not None:
            data['elapsed']['value'] = elapsed.waiit(now, pk)
            data['elapsed']['percent'] = elapsed.get_elapsed(now, pk)
            serializer = ElapsedSerializer(instance=data)
        else:
            data['elapsed']['value'] = elapsed.waiit(now)
            data['elapsed']['percent'] = elapsed.get_elapsed(now)
            serializer = ElapsedSerializer(instance=data)



        if (data['elapsed']["value"] is None) or (data["elapsed"]['percent'] is None):
            return Response({"error": "Invalid key"}, status=400)

        
        return Response(serializer.data)