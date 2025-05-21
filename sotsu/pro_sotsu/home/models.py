from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class StoreAccountManager(BaseUserManager):
    def create_user(self, store_name, password=None, **extra_fields):
        if not store_name:
            raise ValueError("The Store Name must be set")
        user = self.model(store_name=store_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, store_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(store_name, password, **extra_fields)

class StoreAccount(AbstractBaseUser):
    store_name = models.CharField(max_length=100, unique=True)
    postal_code = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    manager_name = models.CharField(max_length=100)
    manager_email = models.EmailField(unique=True)
    manager_phone = models.CharField(max_length=15)
    registration_date = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = StoreAccountManager()

    USERNAME_FIELD = 'store_name'
    REQUIRED_FIELDS = ['manager_email']
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.store_name
