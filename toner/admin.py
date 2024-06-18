from django.contrib import admin
from .models import *
from custom_auth.models import CustomUser

# class toneradmin(admin.ModelAdmin):
#     list_display = ('user', 'issued', 'toner', 'Date_of_request')
#     list_filter = ('issued', 'toner', 'Date_of_request')
#     search_fields = ('user__username', 'toner__Toner_name')
# class tonersAdmin(admin.ModelAdmin):
#     list_display = ('toner','quantity')

# admin.site.register(Toner,)
# admin.site.register(Toner_Request,)
# admin.site.register(Printer)

 

