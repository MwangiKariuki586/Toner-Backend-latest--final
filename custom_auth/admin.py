from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Kenindia_Department, Kenindia_Location, Printer, Toner, Toner_Request
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm


class CustomUserAdmin(BaseUserAdmin):
    change_password_form = AdminPasswordChangeForm
    list_display = ('staffid', 'staff_name', 'department', 'location', 'is_staff', 'last_login')
    fieldsets = (
        (None, {'fields': ('staffid','password')}),
        ('Personal Info', {'fields': ('staff_name', 'department', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('staffid', 'staff_name', 'department', 'location', 'password1', 'password2'),
        }),
    )
    search_fields = ('staffid', 'staff_name', 'department', 'location')
    ordering = ('staffid',)
    list_filter = ('department', 'location', 'is_staff', 'is_superuser')

class TonerRequestAdmin(admin.ModelAdmin):
    list_display = ('user_staffname','user_staffid', 'user_department', 'user_location','toner' ,'printer_name','Date_of_request','issued',"days_since_request")
    list_filter = ('Date_of_request',)
    search_fields = ('user_staffname', 'user_department', 'user_location')
    actions = ['set_request_to_issued']
    def user_staffname(self, obj):
        return obj.user_staffname if obj.user_staffname else 'Unassigned'

    user_staffname.short_description = 'User Staffname'

    def user_department(self, obj):
        return obj.user_department if obj.user_department else 'Unassigned'

    user_department.short_description = 'User Department'

    def user_location(self, obj):
        return obj.user_location if obj.user_location else 'Unassigned'

    user_location.short_description = 'User Location'

    def save_model(self, request, obj, form, change):
        # Set user-related fields based on the logged-in user
        if not obj.user_staffid:
            obj.user_staffid = request.user.staffid
            obj.user_staffname = request.user.staff_name
            obj.user_department = request.user.department
            obj.user_location = request.user.location

        super().save_model(request, obj, form, change)
    

    def set_request_to_issued(self, request, queryset):
        queryset.update(issued=True)

    set_request_to_issued.short_description = "Set selected requests to issued"  # Set custom action description

# Register the custom user model with the CustomUserAdmin

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Kenindia_Department)
admin.site.register(Kenindia_Location)
admin.site.register(Toner,)
admin.site.register(Toner_Request,TonerRequestAdmin)
admin.site.register(Printer)
