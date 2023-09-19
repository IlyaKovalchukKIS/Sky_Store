from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView
from catalog.models import Product, Category, Version
from catalog.forms import ProductForm, CategoryForm, VersionForm
from django.urls import reverse_lazy
from config.utils import ValidMixin, VersionViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


class IndexTemplateView(VersionViewMixin, TemplateView):
    model = Product
    success_url = reverse_lazy('catalog:index')


def contacts(request):
    return render(request, 'catalog/contacts.html')


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, ValidMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:category_list')


class ProductListView(VersionViewMixin, ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Product.objects.filter(category_id=category_id)


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_version: Version = Version.objects.filter(product=self.object, is_active=True).last()
        if active_version:
            context['is_active'] = active_version.is_active
            context['version'] = active_version.version
            context['name_version'] = active_version.name_version
        else:
            context['version'] = None
            context['name_version'] = None

        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, ValidMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:category_list')

    def test_func(self):
        # Проверка, является ли текущий пользователь создателем продукта или модератором
        product = self.get_object()
        return (self.request.user == product.user
                or self.request.user.is_staff
                or self.request.user.is_superuser)


class ProductDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:category_list')


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, ValidMixin, CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'category.add_category'
    success_url = reverse_lazy('catalog:category_list')


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Обработка описания категорий
        for category in context['categories']:
            if len(category.description) > 100:
                category.description = category.description[:100] + '...'  # Ограничение до 100 символов

        return context


class CategoryDetailView(DetailView):
    model = Product
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, ValidMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'catalog.change_category'
    success_url = reverse_lazy('catalog:category_list')


class CategoryDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Category
    permission_required = 'catalog.delete_category'
    success_url = reverse_lazy('catalog:category_list')


class VersionCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.create_version'
    success_url = reverse_lazy('catalog:category_list')
