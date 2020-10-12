from django.contrib import admin
from .models import Politician
# Register your models here.
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ('name', 'othername')
admin.site.register(Politician, PoliticianAdmin)
