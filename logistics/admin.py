from django.contrib import admin
from .models import Dock, Robot, LogisticsData

# 註冊模型以便於後台管理
admin.site.register(Dock)
admin.site.register(Robot)
admin.site.register(LogisticsData)
