from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Flavor, IceCream, Order , CustomUser

admin.site.register(Flavor)
admin.site.register(IceCream)
admin.site.register(Order)
admin.site.register(CustomUser)



