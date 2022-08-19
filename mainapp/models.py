from django.db import models

# Create your models here.

class usercsv(models.Model):
    Email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.Email

class file(models.Model):
    file = models.FileField()
    user=models.ForeignKey(usercsv, null=True, on_delete=models.SET_NULL)