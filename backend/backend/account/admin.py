from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # Fields to display in the list view
    list_display = ('email', 'name', 'company', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')

    # Search fields for admin search bar
    search_fields = ('email', 'name', 'company')
    ordering = ('email',)

    # Fields to display in the user detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'company', 'avatar')}),  # Added company here
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'company', 'avatar', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')