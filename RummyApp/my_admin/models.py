from django.db import models
from app.models import User
# Create your models here.



class Game1(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    point_value = models.CharField(max_length=100)
    no_of_players = models.IntegerField()
    rummy_type = models.CharField(max_length=200)
    active =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)