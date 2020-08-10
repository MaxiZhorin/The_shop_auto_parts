from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductGroupImageInline(admin.TabularInline):
    model = ProductGroupImage
    extra = 0


class ProductCross(admin.TabularInline):
    model = ProductCross
    extra = 1


class ProductAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductImageInline, ProductCross]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)

class Group_admin (admin.ModelAdmin):
    list_display = [field.name for field in ProductGroup._meta.fields]
    inlines = [ProductGroupImageInline]

    class Meta:
        model = ProductGroup

admin.site.register(ProductGroup, Group_admin)

class ProductGroupImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductGroupImage._meta.fields]


    class Meta:
        model = ProductGroupImage

admin.site.register(ProductGroupImage, ProductGroupImageAdmin)