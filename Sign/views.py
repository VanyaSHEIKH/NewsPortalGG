from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from News.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group, created = Group.objects.get_or_create(name='author')

    # Проверяем, состоит ли пользователь в группе 'author'
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)

    # Проверяем, существует ли уже объект Author для данного пользователя
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)

    return redirect('/posts/')
