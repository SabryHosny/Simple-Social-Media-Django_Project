from enum import unique
from django.db import models
from django.urls import reverse
from django.conf import settings

# import misaka

from groups.models import Group  # so we can connect a post to an actual group

from django.contrib.auth import get_user_model
User = get_user_model()  # to connect the cuurent post to who logged as a user

# Create your models here.


class Post(models.Model):
    # 1) setup the atteributes of Post
    # 2) setup the representation method __str__
    # 3) setup the save method
    # 4) setup the get_absolute_url method which means when some one create a post where we should send him
    # 5) and the Meta class for other information

    user = models.ForeignKey(User, related_name='posts',
                             on_delete=models.CASCADE)

    group = models.ForeignKey(
        Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        # self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:single", kwargs={'username': self.user.username, "pk": self.pk})

    class Meta:
        # decending order, so the most recent posts comes first
        ordering = ['-created_at']
        unique_together = ['user', 'message']
