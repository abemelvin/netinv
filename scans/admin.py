from django.contrib import admin
from .models import Device, Scan, Host, Interface



class HostAdmin(admin.ModelAdmin):
    model = Host
    filter_horizontal = ('access_interface', 'scans_found',)


admin.site.register(Device)
admin.site.register(Scan)
admin.site.register(Host, HostAdmin)
admin.site.register(Interface)