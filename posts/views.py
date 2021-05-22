from django.contrib import auth
from django.db.models.fields import mixins
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin

from django.http import Http404
from . import models, forms

from django.contrib.auth import get_user_model
User = get_user_model()
# when some one logged in to a session i'm going to be able to use this User object
# as the current user and then call things of of that

# Create your views here.


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group')


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            # try to get posts of the user you happen to click on
            # this is just to make sure that when you call the queryset for the user posts that the user actaully
            # exist and you able to fetch the posts that are related to that user
            # iexact : Case-insensitive exact match
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username"))

        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    # join those related tables with the Post table in (one table)
    select_related = ("user", "group")
    # so i can call there fields directly like ex: self.kwargs.get("username")
    # instead self.user.kwargs.get("username")

    def get_queryset(self):
        # first we get all posts then we will filter them
        queryset = super().get_queryset()
        # user__username__iexact => the 'username' of the joined related table 'user'
        # self.kwargs.get("username") => the username of the user that we will pass to PostDetail
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatPost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Post
    fields = ('message', 'group')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
