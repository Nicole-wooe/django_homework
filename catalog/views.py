from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Category, Product
from catalog.services import get_products_by_category


class HomeView(TemplateView):
    template_name = "catalog/home.html"


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


class ProductsByCategoryView(ListView):
    model = Product
    template_name = "catalog/products_by_category.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs["category_id"]

        context["category"] = get_object_or_404(
            Category,
            pk=category_id,
        )

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView,
):
    model = Product
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        product = self.get_object()

        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.has_perm(
            "catalog.can_unpublish_product"
        )

        return is_owner or is_moderator

    def get_form_class(self):
        product = self.get_object()

        if product.owner == self.request.user:
            return ProductForm

        return ProductModeratorForm

    def handle_no_permission(self):
        raise PermissionDenied(
            "Редактировать продукт может только его владелец "
            "или модератор."
        )


class ProductDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        product = self.get_object()

        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.has_perm(
            "catalog.delete_product"
        )

        return is_owner or is_moderator

    def handle_no_permission(self):
        raise PermissionDenied(
            "Удалять продукт может только его владелец "
            "или модератор."
        )
