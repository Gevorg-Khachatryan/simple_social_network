from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(User):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    friends = models.ManyToManyField('self', related_name='friends')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.username

    def add_friend(self, user):
        self.friends.add(user)

    def delete_friend(self, user):
        self.friends.remove(user)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField('Title', max_length=32)
    content = models.TextField('Content')
    creator = models.ForeignKey(CustomUser, related_name='created_by_%(class)s_related', on_delete=models.CASCADE)
    like = models.ManyToManyField(CustomUser, blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pk']


class Comment(models.Model):
    comment = models.TextField('Comment')
    author = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)


class FriendRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PD', _('Pending')
        APPROVED = 'AD', _('Approved')
        REJECTED = 'RD', _('Rejected')

    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)

    def approve_request(self):
        self.sender.add_friend(self.recipient)
        self.delete()

    def reject_request(self):
        self.status = self.Status.REJECTED
