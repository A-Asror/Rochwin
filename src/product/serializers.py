from rest_framework import serializers


__all__ = [
    "VendorStatisticsQueryParamsSerializer",
    "VendorStatisticsSerializer",
    "CustomerStatisticsQueryParamsSerializer",
    "CustomerStatisticsSerializer"
]


class VendorStatisticsQueryParamsSerializer(serializers.Serializer):
    month: int = serializers.IntegerField(min_value=0)
    year: int = serializers.IntegerField(min_value=1900)


class CustomerStatisticsQueryParamsSerializer(serializers.Serializer):
    month: int = serializers.IntegerField(min_value=0)
    year: int = serializers.IntegerField(min_value=1900)


class VendorStatisticsSerializer(serializers.Serializer):
    fullname = serializers.CharField(source="vendor__fullname")
    customers = serializers.IntegerField()
    products = serializers.IntegerField()
    sales_amount = serializers.FloatField()


class CustomerStatisticsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="customer_id")
    fullname = serializers.CharField(source="customer__fullname")
    products = serializers.IntegerField()
    sales_amount = serializers.FloatField()
    pass
