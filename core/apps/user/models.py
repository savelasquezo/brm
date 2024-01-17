import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('¡Email Obligatorio!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(_("ID"),default=uuid.uuid4, unique=True, primary_key=True)
    username = models.CharField(_("Usuario"),max_length=64, unique=True)
   
    first_name = models.CharField(_("Nombre"), max_length=150, null=False, blank=False)
    last_name = models.CharField(_("Apellido"), max_length=150, null=False, blank=False)
    email = models.EmailField(_("Email"),unique=True)
    phone = models.CharField(_("Telefono"),max_length=64, unique=True, null=False, blank=False)
    
    street = models.CharField(_("Direccion"),max_length=128, unique=False, null=True, blank=True)
    city = models.CharField(_("Ciudad"),max_length=128, unique=False, null=True, blank=True)
    postal_code = models.CharField(_("Postal"),max_length=128, unique=False, null=True, blank=True)
    country = models.CharField(_("Pais"),max_length=128, unique=False, null=True, blank=True)

    date_joined = models.DateField(_("Fecha Ingreso"),default=timezone.now)
    last_joined = models.DateField(_("Ultimo Ingreso"),default=timezone.now)
   
    is_active = models.BooleanField(_("¿Activo?"),default=True)
    is_staff = models.BooleanField(_("¿Administrador?"),default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email}"

    class Meta:
        indexes = [models.Index(fields=['email']),]
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
