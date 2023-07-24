from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import OrderModel, ProductModel


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = "__all__"

    def clean(self):
        product: ProductModel = self.cleaned_data['product']
        if (quantity := product.quantity - self.cleaned_data['quantity']) < 0:
            raise forms.ValidationError("Invalid quantity value. Not enough goods.")
        self.cleaned_data['sum'] = self.cleaned_data['quantity'] * product.price
        product.save(update={"quantity": quantity}, update_fields=("quantity",))
        return self.cleaned_data


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor_id', "customer_id", "product_id")  # 'username',
    list_display_links = ('id', "vendor_id", "customer_id")
    readonly_fields = ("sum", "product", "quantity")
    form = OrderForm
    fieldsets = (
        ('Editable', {
            'fields': ('vendor', "customer")
        }),
        ('Read Only', {
            'fields': ('sum', "product", "quantity")
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ["sum"]
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj: OrderModel, form, change):
        obj.sum = form.cleaned_data['sum']
        super().save_model(request, obj, form, change)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', "price", "quantity")  # 'username',
    list_display_links = ('id', "title")
    fieldsets = (
        ('Editable', {
            'fields': ('title', "quantity")
        }),
        ('Read Only', {
            'fields': ('price',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ["price"]
        return super().get_readonly_fields(request, obj)
