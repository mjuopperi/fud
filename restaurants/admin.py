from django.contrib import admin
from restaurants import models

# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Restaurant, RestaurantAdmin)
