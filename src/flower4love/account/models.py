from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    scores = models.IntegerField(default=0)
    mobile_phone = models.CharField(max_length=11, null=True, blank=True)
    user_image = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.real_name
