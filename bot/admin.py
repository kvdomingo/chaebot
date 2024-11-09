from django.contrib import admin

from bot.models import Comeback, ScheduleSubscriber

admin.site.register(Comeback)
admin.site.register(ScheduleSubscriber)

admin.site.index_title = "Admin"
admin.site.site_title = "ChaeBot"
admin.site.site_header = "ChaeBot Administration"
