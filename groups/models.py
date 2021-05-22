from django import template
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# import misaka
from django.contrib.auth import get_user_model
User = get_user_model()  # it allows me to call things of the current user session

register = template.Library()

# Create your models here.

# ## NOTE:
# scince the relationship between User & Group is many-to-many,
# so we create the GroupMember to devide this relationship into two one-to-one
# User >-----------------------------< Group "convert many-to-many into 2 one-to-one" :
# User-------< GroupMember >-----------Group


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(
        Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
