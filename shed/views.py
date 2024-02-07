from django.shortcuts import render
import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from blog.models import Blog
from shed.forms import MailForm, MessageForm, ClientForm, MailModeratorForm
from shed.models import Message, Mail, Client, Logs
from shed.services import get_cache_for_mail, get_cache_for_active_mail


# Create your views here.

class MailCreateView(LoginRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('shed:mail_list')
    extra_context = {
        'title': 'Создание рассылки'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form_instance):
        new_mail = form_instance.save(commit=False)
        new_mail.user = self.request.user
        new_mail.save()
        return super().form_valid(form_instance)


class MailUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('shed:mail_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return self.request.user == Mail.objects.get(pk=self.kwargs['pk']).owner


class MailUpdateModeratorView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mail
    form_class = MailModeratorForm
    success_url = reverse_lazy('shed:mail_list')
    permission_required = 'shed.set_is_active'


class MailListView(LoginRequiredMixin, ListView):
    model = Mail
    extra_context = {
        'title': 'Список рассылок'
    }


class HomeView(ListView):
    model = Mail
    template_name = 'shed/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mail_count'] = get_cache_for_mail()
        context_data['active_mail_count'] = get_cache_for_active_mail()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        context_data['clients_count'] = len(Client.objects.all())
        return context_data


class MailDetailView(DetailView):
    model = Mail

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = list(self.object.client.all())
        context_data['logs'] = list(Logs.objects.filter(mailing=self.object))
        return context_data


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('shed:mail_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('shed:message_list')
    extra_context = {
        'title': 'Создание сообщения'
    }

    def form_valid(self, form):
        new_message = form.save()
        new_message.user = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('shed:message_view', args=[self.kwargs.get('pk')])


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Список сообщений'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = Message.objects.filter(user=self.request.user)
        return queryset


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('shed:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = Client.objects.filter(user=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('shed:client_list')
    extra_context = {
        'title': 'Добавить клиента'
    }

    def form_valid(self, form):
        new_client = form.save()
        new_client.user = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('shed:client_list')

    def test_func(self):
        return self.request.user == Client.objects.get(pk=self.kwargs['pk']).user