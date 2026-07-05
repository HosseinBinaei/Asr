from rest_framework import serializers
from core.models import Note
from core.utils import jalali_now
import jdatetime

class TimeSerializer(serializers.Serializer):
    now = serializers.JSONField()

class ElapsedSerializer(serializers.Serializer):
    now = serializers.JSONField()
    elapsed = serializers.JSONField()


class NoteSerializer(serializers.ModelSerializer):

    created_at = serializers.CharField(required=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'note_type', 'created_at']

    def validate_created_at(self, value):
        try:
            clean_value = value.replace("/", "-")
            parts = clean_value.split("-")

            if len(parts) != 3:
                raise ValueError

            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
        except (ValueError, IndexError):
            raise serializers.ValidationError(
                "فرمت تاریخ نامعتبر است. لطفاً به صورت YYYY-MM-DD وارد کنید (مثال: 1404-5-5 یا 1404-05-05)"
            )

        now = jalali_now()

        try:
            combined_datetime = jdatetime.datetime(
                year=year,
                month=month,
                day=day,
                hour=now.hour,
                minute=now.minute,
                second=now.second,
                tzinfo=now.tzinfo,
            )
        except ValueError as e:
            raise serializers.ValidationError(
                f"تاریخ وارد شده در تقویم جلالی وجود ندارد: {str(e)}"
            )

        return combined_datetime