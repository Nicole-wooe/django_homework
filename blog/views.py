from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    model = Blog
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )
    success_url = reverse_lazy("blog:list")


class BlogUpdateView(UpdateView):
    model = Blog
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )

    def get_success_url(self):
        return reverse(
            "blog:detail",
            args=[self.object.pk],
        )


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:list")
