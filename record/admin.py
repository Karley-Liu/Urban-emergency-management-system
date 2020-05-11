from django.contrib import admin

# Register your models here.
from record import models
from record.views import record


class MyAdminSite(admin.AdminSite):
    pass

@admin.register(models.Recording)
class RecordAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return record(request)

@admin.register(models.Record)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','video_url','datetime')
    list_per_page = 6
    list_filter = ('datetime',)

    class Media:
        js = ('admin/js/vendor/jquery/jquery-3.4.1.min.js', 'admin/js/thisVideo.js')