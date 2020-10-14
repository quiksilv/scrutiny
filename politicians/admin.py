from django.contrib import admin
from .models import Politician, Constituency, Appointment
# Register your models here.
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ('name', 'othername')
admin.site.register(Politician, PoliticianAdmin)
admin.site.register(Constituency)
admin.site.register(Appointment)
