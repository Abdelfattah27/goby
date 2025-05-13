from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from .forms import UserAdminForm

admin.site.register(Employee)
admin.site.register(EmployeeType)
admin.site.register(Nationality)
admin.site.register(City)
admin.site.register(MaritalStatus)
admin.site.register(CityDistrict)
admin.site.register(Moderator)
admin.site.register(User, UserAdminForm)
# admin.site.unregister(Group)
