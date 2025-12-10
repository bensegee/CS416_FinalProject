from django.db import models

# Create your models here.
class Comment(models.Model):
   event = models.CharField(max_length=100)
   user = models.CharField(max_length=50)
   comment = models.CharField(max_length=500)


   def __str__(self):
       return self.event
