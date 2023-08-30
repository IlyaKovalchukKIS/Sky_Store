from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductCreateView, ProductListView, ProductDetailView, ProductUpdateView, \
    ProductDeleteView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView, CategoryDetailView, CategoryListView, \
    contacts, VersionCreateView, IndexTemplateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexTemplateView.as_view(template_name='catalog/product_list.html'), name='index'),
    path('contacts/', contacts, name='contacts'),

    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/view/<int:pk>', ProductDetailView.as_view(), name='product_view'),
    path('product/edit/<int:pk>', ProductUpdateView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),

    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/list/',  CategoryListView.as_view(), name='category_list'),
    path('category/view/<int:pk>',  ProductListView.as_view(), name='category_view'),
    path('category/edit/<int:pk>',  CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>', CategoryDeleteView.as_view(), name='category_delete'),

    path('version/create/', VersionCreateView.as_view(), name='version_create'),
]
