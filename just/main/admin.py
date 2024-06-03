from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserChangeForm


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

    list_display = ('email', 'phone', 'role', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'avatar', 'city', 'birthday', 'company')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'role', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('email', 'phone', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)



