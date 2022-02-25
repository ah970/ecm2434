from django.db import models

# Create the user model
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
