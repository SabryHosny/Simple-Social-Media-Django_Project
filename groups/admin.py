from django.contrib import admin
from . import models


# Register your models here.

# ### TabularInline class into admin.py:
# allows us to utilize the admin interface in our django admin website with the ability
# to edit models in the same page as the parent model.
# >> so the (GroupMember) has a bit of a parent model with (Group), so we can use a TabularInline class,
# so when we visit the admin page we can click on Group and can see the GroupMembers and edit these as well.

class GroupMemeberInline(admin.TabularInline):
    model = models.GroupMember


admin.site.register(models.Group)
