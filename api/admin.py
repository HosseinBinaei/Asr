from django.contrib import admin
from core.models import CustomUser, Note

admin.site.register(CustomUser)
admin.site.register(Note)
