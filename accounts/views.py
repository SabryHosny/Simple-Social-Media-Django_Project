from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from . import models, forms


# Create your views here.
class SignUp(CreateView):
    # 1) which model to create into Db
    # model = models.User  => I think CreateView will automatically make this model
    # from the model of the form, so we don't need that :)

    # 2) form used to create
    form_class = forms.UserCreateForm
    # 3) template url
    template_name = 'accounts/signup.html'
    # 4) success url to redirect
    success_url = reverse_lazy('login')
