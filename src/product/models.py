from django.db import models
from django.conf import settings


from src.base.models import BaseModel


__all__ = ["ProductModel", "OrderModel"]


class ProductModel(BaseModel):
    title: str = models.CharField(max_length=255, db_column="title")
    price: float = models.DecimalField(max_digits=10, decimal_places=2, db_column="price")
    quantity: int = models.IntegerField(db_column="quantity")

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class OrderModel(BaseModel):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="vendor_orders")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="customer_orders")
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, related_name="orders")
    quantity: int = models.IntegerField(db_column="quantity")
    sum: float = models.DecimalField(max_digits=10, decimal_places=2, db_column="sum")

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
