from django.contrib.auth import models as auth_models
from django.db.models.manager import EmptyManager
from django.utils.functional import cached_property

from .compat import CallableFalse, CallableTrue
from .settings import api_settings


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, mobile, first_name = None, last_name = None, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not mobile:
            raise ValueError(_("The mobile must be set"))

        if not username:
            raise ValueError(_("The username must be set"))
        
        user = self.model(username=username, mobile=mobile, first_name = first_name, last_name = last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username, mobile, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_customer", False)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user( username=username, mobile=mobile, password=password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    mobile = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True )
    customer_number = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=200, blank=True, null=True)
    otp = models.CharField(max_length=200, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()


    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["mobile"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class TokenUser:
    """
    A dummy user class modeled after django.contrib.auth.models.AnonymousUser.
    Used in conjunction with the `JWTStatelessUserAuthentication` backend to
    implement single sign-on functionality across services which share the same
    secret key.  `JWTStatelessUserAuthentication` will return an instance of this
    class instead of a `User` model instance.  Instances of this class act as
    stateless user objects which are backed by validated tokens.
    """

    # User is always active since Simple JWT will never issue a token for an
    # inactive user
    is_active = True

    _groups = EmptyManager(auth_models.Group)
    _user_permissions = EmptyManager(auth_models.Permission)

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return f"TokenUser {self.id}"

    @cached_property
    def id(self):
        return self.token[api_settings.USER_ID_CLAIM]

    @cached_property
    def pk(self):
        return self.id

    @cached_property
    def username(self):
        return self.token.get("username", "")

    @cached_property
    def mobile(self):
        return self.token.get("mobile", "")

    @cached_property
    def first_name(self):
        return self.token.get("first_name", "")

    @cached_property
    def last_name(self):
        return self.token.get("last_name", "")

    @cached_property
    def customer_number(self):
        return self.token.get("customer_number", "")

    @cached_property
    def is_staff(self):
        return self.token.get("is_staff", False)

    @cached_property
    def is_superuser(self):
        return self.token.get("is_superuser", False)

    @cached_property
    def is_customer(self):
        return self.token.get("is_customer", False)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    def save(self):
        raise NotImplementedError("Token users have no DB representation")

    def delete(self):
        raise NotImplementedError("Token users have no DB representation")

    def set_password(self, raw_password):
        raise NotImplementedError("Token users have no DB representation")

    def check_password(self, raw_password):
        raise NotImplementedError("Token users have no DB representation")

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        return False

    def has_module_perms(self, module):
        return False

    @property
    def is_anonymous(self):
        return CallableFalse

    @property
    def is_authenticated(self):
        return CallableTrue

    def get_username(self):
        return self.username

    def __getattr__(self, attr):
        """This acts as a backup attribute getter for custom claims defined in Token serializers."""
        return self.token.get(attr, None)



