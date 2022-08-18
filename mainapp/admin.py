from django.contrib import admin
from .models import temp, file, usercsv

# Register your models here.
admin.site.register(temp)

admin.site.register(usercsv)

admin.site.register(file)