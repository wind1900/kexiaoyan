from django.contrib import admin
import models

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('category', 'content', 'time')
    list_display_links = ('content',)
    ordering = ('-time',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    ordering = ('-date',)

admin.site.register(models.Category)
admin.site.register(models.Material, MaterialAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Memday)
admin.site.register(models.Birthday)
admin.site.register(models.FetionText)
