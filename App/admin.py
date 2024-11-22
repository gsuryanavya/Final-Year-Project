from django.contrib import admin

# Register your models here.
from .models import FetalHealthData,UserImageModel

admin.site.register(FetalHealthData)
admin.site.register(UserImageModel)