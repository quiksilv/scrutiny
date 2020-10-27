from django.contrib import admin
from .models import Statistics
# Register your models here.
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'value', 'politician', 'created')
    date_hierarcy = '-created'
admin.site.register(Statistics, StatisticsAdmin)
