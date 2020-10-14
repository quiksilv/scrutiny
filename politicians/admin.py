from django.contrib import admin
from .models import Politician, Constituency, Portfolio
# Register your models here.
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'state')
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ('name', 'othername')
admin.site.register(Politician, PoliticianAdmin)
admin.site.register(Constituency, ConstituencyAdmin)
admin.site.register(Portfolio)
