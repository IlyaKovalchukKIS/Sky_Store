from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from catalog.models import Product, Category
from catalog.forms import ProductForm, CategoryForm
from django.urls import reverse_lazy


def index(request):
    context = {
        'object_list': Product.objects.all()[:3],
        'title': 'Топ товаров'
    }

    return render(request, 'catalog/product_list.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        if image:
            new_product = form.save(commit=False)
            new_product.image = image
            new_product.save()
        else:
            form.save()

        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Product.objects.filter(category_id=category_id)


class ProductDetailView(DetailView):
    model = Product


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        if image:
            new_product = form.save(commit=False)
            new_product.image = image
            new_product.save()
        else:
            form.save()

        return super().form_valid(form)


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


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('catalog:category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:category_list')
