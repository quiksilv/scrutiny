from django.contrib import admin
from .models import Hansard, Paragraph

# Register your models here.
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('hansard', 'page', 'line', 'content', 'politician')
admin.site.register(Hansard)
admin.site.register(Paragraph, ParagraphAdmin)
