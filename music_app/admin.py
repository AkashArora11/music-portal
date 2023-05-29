from django.contrib import admin
from .models import MusicFile
from django.utils.html import format_html

# Register your models here.


class MusicFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_file_link', 'upload_type', 'user')

    def display_file_link(self, obj):
        return format_html('<a href="{0}">{1}</a>', obj.file.url, obj.file.name)

    display_file_link.short_description = 'File Link'


admin.site.register(MusicFile, MusicFileAdmin)
