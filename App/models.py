from django.db import models
from django.contrib.auth.models import User
from PIL import Image



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    
class UserImageModel(models.Model):
    image = models.ImageField(upload_to = 'images/',blank=True)
    label = models.CharField(max_length=20,default='data')
    def __str__(self):
        return str(self.image)
    

from django.db import models

class FetalHealthData(models.Model):
    LBE = models.IntegerField()
    LB = models.IntegerField()
    AC = models.IntegerField()
    FM = models.IntegerField()
    UC = models.IntegerField()
    ASTV = models.IntegerField()
    MSTV = models.IntegerField()
    ALTV = models.IntegerField()
    MLTV = models.IntegerField()
    DL = models.IntegerField()
    DS = models.IntegerField()
    DP = models.IntegerField()
    DR = models.IntegerField()
    Width = models.IntegerField()
    Min = models.IntegerField()
    Max = models.IntegerField()
    Nmax = models.IntegerField()
    Nzeros = models.IntegerField()
    Mode = models.IntegerField()
    Mean = models.IntegerField()
    Median = models.IntegerField()
    Variance = models.IntegerField()
    Tendency = models.IntegerField()
    SUSP = models.IntegerField()
    CLASS = models.IntegerField()
    label=models.CharField(max_length=200)

    def __str__(self):
         return f" Prediction  - {self.label}"
