from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User

from src.base.models import BaseModel, BaseEnum


class RoleChoice(BaseEnum):
    Vendor = "vendor"
    Customer = "customer"


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise TypeError("Users must have a email.")

        if password is None:
            raise TypeError("Both password fields must be filled")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    email: str = models.EmailField(db_index=True, unique=True, db_column="email")
    fullname: str = models.CharField(max_length=150, db_column="fullname")
    dob: int = models.IntegerField(default=20, db_column="day_of_birth")  # day of birth
    role: str = models.CharField(max_length=20, choices=RoleChoice.get_choice(), default="customer", db_column="role")
    is_active: bool = models.BooleanField(default=True, db_column="is_active")
    is_superuser: bool = models.BooleanField(default=False, db_column="is_superuser")
    is_staff: bool = models.BooleanField(default=False, db_column="is_staff")
    groups = None
    user_permissions = None
    USERNAME_FIELD: str = 'email'
    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f'ID: {self.pk}, email: {self.email}'


class JwtModel(BaseModel):
    user: UserModel = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="jwt", db_column="user")
    access: str = models.TextField(db_column="access")
    refresh: str = models.TextField(db_column="refresh")

    class Meta:
        db_table = "jwt"
        verbose_name = "Jwt"
        verbose_name_plural = "Jwt"

    def __str__(self):
        return "Model: %s username: %s id: %s" % (self.__class__.__name__, self.user.email, self.pk)
