from django.contrib import admin
from .models import Post, Tag
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'created')
    date_hierarchy = 'created'

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
