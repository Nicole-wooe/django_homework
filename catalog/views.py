from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product


class HomeView(TemplateView):
    template_name = "catalog/home.html"


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"


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
