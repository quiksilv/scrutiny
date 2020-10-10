from django.contrib import admin
from .models import Agency, Source

# Register your models here.
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('headline', 'source', 'created')
    date_hierarchy = 'created'

admin.site.register(Agency, AgencyAdmin)
admin.site.register(Source)
