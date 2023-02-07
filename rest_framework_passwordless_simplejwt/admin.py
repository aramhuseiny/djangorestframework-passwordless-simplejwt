from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User 
from .forms import CustomUserCreationForm, CustomUserChangeForm


class UserAdmin(DjangoUserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("username", "mobile", "password", "email", "first_name", "last_name", "customer_number", "latitude", "longitude", "date_joined", "is_staff", "is_customer", "is_superuser", "is_active",)

    search_fields = ("username","mobile",)
    ordering = ("mobile",)
    readonly_fields=('date_joined',)
    fieldsets = (
         (None, {
            'classes': ('wide',),
            'fields': ('username', 'mobile', 'first_name', 'last_name', 'email', 'customer_number', 'latitude', 'longitude', 'is_active', 'is_staff', 'is_customer'),
        }),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'mobile',  'password1', 'password2','first_name', 'last_name', 'email', 'customer_number', 'latitude', 'longitude', 'is_active', 'is_staff', 'is_customer'),
        }),
    )
    def change_view(self, request, object_id, extra_context=None):
        if request.user.is_superuser:
            self.exclude = ('password1','password2',)
        else:
            self.exclude = ('mobile', 'password1', 'password2', 'user_permissions', 'groups',)
        return super().change_view(request, object_id, extra_context)
       

admin.site.register(User, UserAdmin)
