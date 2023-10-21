from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a phone number!')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=155, unique=False, null=True, blank=True)
    phone_number = models.CharField(
        max_length=13,  # Change this to match the length of a phone number with country code, e.g., +998123456789
        unique=True,
        validators=[RegexValidator(
            regex=r'^\+998\d{9}$',
            message="Yaroqsiz telefon raqam!"
        )],
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Group(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return self.title


# Bu jarayonda Person modeli ham teacher uchun ham student uchun umumiy !
# Botga oddiy user holatida kirgan insonni student yoki teacher ekanligini is_teacher fieldi orqali check qilamiz !
class Person(models.Model):
    fullname = models.CharField(max_length=155)
    phone_number = models.CharField(max_length=155)
    password = models.CharField(max_length=8)
    group = models.ForeignKey(to='app.Group',
                              on_delete=models.CASCADE,
                              related_name='persons')
    is_teacher = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.fullname
