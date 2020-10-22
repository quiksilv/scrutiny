from django.contrib import admin
from .models import Party, Politician, Constituency, Portfolio
# Register your models here.
class PartyAdmin(admin.ModelAdmin):
    list_display = ('abbr', 'english_name')
class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'state')
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ('name', 'othername')
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'othername')
admin.site.register(Party, PartyAdmin)
admin.site.register(Politician, PoliticianAdmin)
admin.site.register(Constituency, ConstituencyAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
