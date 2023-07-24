from django.db.models import Count, Sum
from rest_framework.generics import RetrieveAPIView
from django.core.exceptions import ValidationError
from django.http import Http404

from src.users.models import RoleChoice
from src.product.models import OrderModel

from .serializers import VendorStatisticsQueryParamsSerializer, VendorStatisticsSerializer, CustomerStatisticsSerializer


class VendorStatisticsAPIView(RetrieveAPIView):
    queryset = OrderModel.objects.select_related("vendor")
    serializer_class = VendorStatisticsSerializer

    def get_object(self):
        pk = self.kwargs[self.lookup_field]
        query_params = VendorStatisticsQueryParamsSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)
        try:
            return (
                self.queryset
                .filter(
                    vendor_id=pk,
                    vendor__role=RoleChoice.Vendor.value,
                    created_at__year=query_params.validated_data['year'],
                    created_at__month=query_params.validated_data['month']
                )
                .values("vendor__fullname")
                .annotate(
                    customers=Count("customer_id", distinct=True),
                    products=Sum("quantity"),
                    sales_amount=Sum("sum")
                )
                .order_by("vendor__fullname")
                .get()
            )
        except (TypeError, ValueError, ValidationError, OrderModel.DoesNotExist) as e:
            raise Http404


class CustomerStatisticsAPIView(RetrieveAPIView):
    queryset = OrderModel.objects.select_related("customer")
    serializer_class = CustomerStatisticsSerializer

    def get_object(self):
        pk = self.kwargs[self.lookup_field]
        query_params = VendorStatisticsQueryParamsSerializer(data=self.request.query_params)
        query_params.is_valid(raise_exception=True)
        try:
            return (
                self.queryset
                .filter(
                    customer_id=pk,
                    customer__role=RoleChoice.Customer.value,
                    created_at__year=query_params.validated_data['year'],
                    created_at__month=query_params.validated_data['month']
                )
                .values("customer__fullname", "customer_id")
                .annotate(
                    products=Sum("quantity"),
                    sales_amount=Sum("sum")
                )
                .get()
            )
        except (TypeError, ValueError, ValidationError, OrderModel.DoesNotExist) as e:
            raise Http404
