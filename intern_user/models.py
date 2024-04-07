from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
 
class InternUserManager(BaseUserManager):
    def create_user(self, email, name, phone, s2c_certified ,password=None):
        """
        Creates and saves a User with the given email, name, and phone.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone = phone,
            s2c_certified = s2c_certified,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone , s2c_certified ,  password=None, password2= None):
        """        
        Creates and saves a superuser with the given email, name, and phone. 
        """
        if password == password2:
            raise ValueError("Password Did't match")
        
        
        user = self.create_user(
            email=email,
            name=name,
            phone=phone,
            password=password,
            s2c_certified = s2c_certified, 
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class InternUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    intern_name = models.CharField(max_length = 300, default = "Simply 2 Cloud")
    phone = models.IntegerField(unique = True)
    address = models.TextField()
    available = models.BooleanField(default=True)
    s2c_certified = models.BooleanField(default=False)
    priority = models.IntegerField(default=1,
        validators = [
            MinValueValidator(1, message="Priority must be at least 1"),
            MaxValueValidator(10, message="Priority cannot be above 10")
        ]
    )
    user_type = models.CharField(max_length = 225)
    online_status = models.CharField(max_length=255, default="Active")
    designation = models.CharField(max_length=255,choices=[
        ("Student", "Student"),
        ("Intern", "Intern"),
        ("Employed", "Employed"),
        ("Self Employed", "Self Employed")
    ], default = "Student")
    user_location = models.CharField(max_length=255, null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    user_create_date = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = InternUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone","s2c_certified"]

    def __str__(self):
        return self.name
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Handle permissions here (if needed)
        return True

    def has_module_perms(self, app_label):
        # Handle module permissions here (if needed)
        return True

    @property
    def is_staff(self):
        # Use the is_superuser field provided by AbstractBaseUser
        return self.is_admin