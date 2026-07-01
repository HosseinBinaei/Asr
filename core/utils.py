from django.utils import timezone
import jdatetime


def jalali_now():
    return jdatetime.datetime.fromgregorian(
        datetime=timezone.localtime()
    )