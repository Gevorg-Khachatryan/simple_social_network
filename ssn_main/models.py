from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(User):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField('Title', max_length=32)
    content = models.TextField('Content')
    creator = models.OneToOneField('CustomUser', related_name='created_by_%(class)s_related', on_delete=models.CASCADE)
    like = models.ManyToManyField(CustomUser, null=True, blank=True)
