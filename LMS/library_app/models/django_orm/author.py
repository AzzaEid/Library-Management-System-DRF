from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=30)
    bio = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name