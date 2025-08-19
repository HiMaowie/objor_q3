from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'active', 'staff', 'admin',
                    'joined_date')
    list_filter = ('active', 'staff', 'admin', 'joined_date')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')


from django.contrib import admin

# Register your models here.
