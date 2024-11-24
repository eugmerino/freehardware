from django.contrib import admin

from systemConfig.models import SystemConfig

#-------- Admin site --------
admin.site.index_title = "Hardware Libre"
admin.site.site_header = "Hardware Libre"
admin.site.site_title = "Hardware Libre"
# ---------------------------

@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'acronym',
        'logo',
    )
    list_display_links = ['name']
    fields = (
        'name',
        'acronym',
        'logo',
    )
    search_fields = ('name', 'acronym',)
    list_per_page = 10
    ordering = ['name']