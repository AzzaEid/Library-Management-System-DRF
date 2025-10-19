from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    joined_date = models.DateField(auto_now_add=True)

    # to be added: is_active, membership_type, etc.

    def __str__(self):
        return self.user.username
