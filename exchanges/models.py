from django.db import models

import time

# Create your models here.
class Nonce(models.Model):
    auth = models.CharField(max_length=500)
    nonce = models.IntegerField()
    
    def __str__(self):
        return self.auth