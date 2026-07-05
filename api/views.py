from core.utils import jalali_now
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import TimeSerializer, ElapsedSerializer, NoteSerializer
from core.services import elapsed
from rest_framework.permissions import IsAuthenticated
from core.models import Note
from rest_framework.generics import ListCreateAPIView
import jdatetime
from django.utils.timezone import get_current_timezone


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
    

class NoteListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        
        date_str = self.kwargs.get('date')
        if date_str:
            clean_value = date_str.replace("/", "-")
            parts = clean_value.split("-")
            
            try:
                if len(parts) == 3:
                    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                    mode = 'day'
                elif len(parts) == 2:
                    year, month = int(parts[0]), int(parts[1])
                    day = 1
                    mode = 'month'
                elif len(parts) == 1:
                    year = int(parts[0])
                    month = 1
                    day = 1
                    mode = 'year'
                else:
                    return queryset.none()
            except (ValueError, IndexError):
                return queryset.none()

            tz = get_current_timezone()
            start_time = jdatetime.datetime(year, month, day, 0, 0, 0, tzinfo=tz)
            
            if mode == 'day':
                end_time = jdatetime.datetime(year, month, day, 23, 59, 59, tzinfo=tz)
            elif mode == 'month':
                next_month = month + 1 if month < 12 else 1
                next_year = year if month < 12 else year + 1
                end_time = jdatetime.datetime(next_year, next_month, 1, 0, 0, 0, tzinfo=tz)
            elif mode == 'year':
                end_time = jdatetime.datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=tz)

            if mode == 'day':
                return queryset.filter(created_at__gte=start_time, created_at__lte=end_time)
            else:
                return queryset.filter(created_at__gte=start_time, created_at__lt=end_time)    
        return queryset

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)