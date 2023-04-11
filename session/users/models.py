from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, **kwargs):    # **kwargs는 받을 인자의 갯수가 정해지지 않았을 때  사용
        user = self.model(userrname=username, **kwargs)
        user.set_password(password)
        user.save()

    def create_normaluser(self, username, password, **kwargs):
        self.create_user(self, username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault("is_superuser", True)
        self.create_user(self, username, password, **kwargs)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'

    username = models.CharField(unique=True, max_length=20)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def is_staff(self):
        return self.is_superuser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname