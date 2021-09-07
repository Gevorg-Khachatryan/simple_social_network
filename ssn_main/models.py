from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField('Title', max_length=32)
    content = models.TextField('Content')
    creator = models.ForeignKey(User, related_name='created_by_%(class)s_related', on_delete=models.CASCADE)
    like = models.ManyToManyField(User, null=True, blank=True)

    class Meta:
        ordering = ['pk']
