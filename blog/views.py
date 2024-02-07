from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from blog.models import Blog
from pytils.translit import slugify

class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    fields = ('title', 'content', 'preview',)
    permission_required = ('blog.add_blog',)
    success_url = reverse_lazy('blog:blog_list')
    model = Blog

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview',)
    permission_required = ('blog.change_blog',)
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get(self, request, pk, **kwargs):
        blog = self.get_object()
        context = {
            'object_list': Blog.objects.filter(pk=pk),
        }
        return render(request, 'blog/blog_detail.html', context)

    def get_object(self, queryset=None):    # Задание 3: при открытии отдельной статьи увеличивать счетчик просмотров;
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = ('blog.delete_blog',)
    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()  # Передача объекта блога в контекст
        return context



