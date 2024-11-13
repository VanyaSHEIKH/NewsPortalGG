from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from datetime import datetime, date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache

from django.conf import settings
from .filters import *
from .models import *
from .forms import *

from django.utils.translation import gettext as _

import pytz  # импортируем стандартный модуль для работы с поясами часовыми


class PostsList(ListView):
    model = Post
    ordering = 'date_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    # def get_context_data(self, **kwargs):
    #     common_timezones = {
    #         "London": "Europe/London",
    #         "Paris": "Europe/Paris",
    #         "New York": "America/New_york",
    #         "Moscow": "Europe/Moscow",
    #         "Singapore": "Asia/Singapore",
    #     }
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
    #     # timezone.now().hour всегда возвращает час по UTC, а нам нужен час в соответствии с выбранным часовым поясом.
    #     context['current_time'] = timezone.localtime(timezone.now())  # передаем в контекс текущее время
    #     context[
    #         'timezones'] = common_timezones.items()  # добавляем в контекст все доступные временные пояса, которые мы добавили
    #     # преобразовывая словарь в список кортежей [(ключ, значение), (...) ,]
    #     # context['timezones'] = pytz.common_timezones # добавляем в контекст все доступные временные пояса в джанго
    #     print(context['current_time'])
    #     return context
    #
    # def post(self, request):
    #     request.session['django_timezone'] = request.POST['timezone']
    #     return redirect('Posts_list')  # это означает что мы после выполнения запроса, а смена часового пояса это запрос
    # # который отправляется на сервер и обновляет страницу, перенаправимся на страницу из urls по name = 'Posts_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_in_page'] = self.paginate_by
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    # добавляем кеширование страницы с новостью
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostsSearch(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'posts_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_field = 'N'
        post.author = self.request.user.author
        today = date.today()
        post_limit = Post.objects.filter(author=post.author, date_in__date=today).count()
        if post_limit >= 10:
            return render(self.request, template_name='post_limit.html', context={'author': post.author})
        post.save()
        # notification_new_post.apply_async([post.pk]) #добавил отправку сообщения о создании, передал первичнй ключ
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_field = 'A'
        post.author = self.request.user.author
        today = date.today()
        post_limit = Post.objects.filter(author=post.author, date_in__date=today).count()
        if post_limit >= 10:
            return render(self.request, template_name='post_limit.html', context={'author': post.author})
        post.save()
        # notification_new_post.apply_async([post.pk]) #добавил отправку сообщения о создании, передал первичнй ключ
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('post.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('post.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('Posts_list')


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscriber.add(user)
#
#     massage = 'Успешная подписка на категорию'
#     return render(request, 'subscribe.html', {'category':category, 'massage':massage})
#
#
# @login_required
# def unsubscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscriber.remove(user)
#
#     massage= 'Вы успешно отписались категории'
#     return render(request,'unsubscribe.html', {'category':category, 'massage':massage})


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscriber.add(user)

    send_mail(
        'Подписка на категорию',
        f'Вы успешно подписались на категорию: {category.category}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    massage = 'Успешная подписка на категорию'
    return render(request, 'subscribe.html', {'category': category, 'massage': massage})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    category.subscriber.remove(user)

    send_mail(
        'Отписка от категории',
        f'Вы успешно отписались от категории: {category.category}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    massage = 'Вы успешно отписались категории'
    return render(request, 'unsubscribe.html', {'category': category, 'massage': massage})


class Index(View):
    def get(self, request):
        curent_time = timezone.now()

        # .  Translators: This message appears on the home page only
        models = Category.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/posts/categories')