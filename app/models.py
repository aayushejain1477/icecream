from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    customer = models.CharField(max_length=50, blank=True, null=True)

    # Provide custom related names for groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='custom_users'  # Custom related name for groups
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_users'  # Custom related name for user permissions
    )

    def __str__(self):
        return self.username


class Flavor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IceCream(models.Model):
    name = models.CharField(max_length=100)
    flavor = models.ForeignKey(Flavor, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('done', 'Done'),
        ('inprocess', 'In Process'),
        ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    icecreams = models.ManyToManyField(IceCream)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.pk} by {self.user.username}"