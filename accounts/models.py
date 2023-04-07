from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class AccountsModel(AbstractUser):
    class Meta:
        db_table = "accounts"
