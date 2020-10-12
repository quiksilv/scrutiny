from django.contrib import admin
from .models import Agency, Source

# Register your models here.
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('headline', 'source', 'guid', 'published')
    date_hierarchy = 'published'

admin.site.register(Agency, AgencyAdmin)
admin.site.register(Source)
