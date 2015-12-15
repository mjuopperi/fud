from django.contrib import admin
from restaurants import models


# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'owner')
    pass


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'restaurant')
    pass

admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Menu, MenuAdmin)
