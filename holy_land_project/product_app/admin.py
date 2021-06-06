from django.contrib import admin
from django.db.models import fields
from .models import *
# from related_admin import RelatedFieldAdmin
# from related_admin import getter_for_related_field

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    fields = ('title','price','desc','category','img')
    list_display = ('title','price','category')

# class CategoryAdmin(RelatedFieldAdmin):
#     # fields = ('title')
#     list_display = ('title','product_categories__all')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

