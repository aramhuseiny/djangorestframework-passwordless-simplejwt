from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "role",  "mobile", "email", "first_name", "last_name", "customer_number", "latitude", "longitude", "date_joined", "is_staff", "is_customer", "is_superuser", "is_active",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username","role",  "mobile", "email", "first_name", "last_name", "customer_number", "latitude", "longitude", "date_joined", "is_staff", "is_customer", "is_superuser", "is_active",)