

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _





class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """
        Creates and saves a Superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(
        _("email"),
        unique=True,
        max_length=255,
        blank=False,
        error_messages={
            "unique": _("This email is already registered. Please log in or use a different email.")
        }
    )
  
    is_admin=models.BooleanField(_("admin"),default=False)
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[] 
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email







