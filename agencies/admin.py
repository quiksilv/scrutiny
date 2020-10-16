from django.contrib import admin
from .models import Agency, Source
from .forms import *

# Register your models here.
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('headline', 'source', 'guid', 'published')
    date_hierarchy = 'published'
class SourceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': ImageWidget},
    }

admin.site.register(Agency, AgencyAdmin)
admin.site.register(Source, SourceAdmin)

admin.site.site_header = 'Scrutiny'
