from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group, GroupMember
from . import models


# Create your views here.

class GroupCreate(LoginRequiredMixin, generic.CreateView):
    # go to group_form.html with a {'form':form} to create a new object from Group model
    model = Group
    fields = ('name', 'description')


class SingleGroup(generic.DetailView):
    # go to group_detail.html with a singel object from Group objects 'group' so you can show its properties.
    # filtered by the key attribute send through url
    model = Group


class listGroup(generic.ListView):
    # go to group_list.html with a list of objects 'object_list' created from Group model
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    # get the group that i'm trying to join
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(
                self.request, ("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(
                self.request, "You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
