from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['pk']


class Post(models.Model):
    title = models.CharField('Title', max_length=32)
    content = models.TextField('Content')
    creator = models.ForeignKey('CustomUser', related_name='created_by_%(class)s_related', on_delete=models.CASCADE)
    like = models.ManyToManyField(CustomUser, null=True, blank=True)

    class Meta:
        ordering = ['pk']
