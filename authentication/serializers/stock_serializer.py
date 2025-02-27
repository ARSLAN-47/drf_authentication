from rest_framework import serializers


class StockSerializer(serializers.Serializer):
    stock_name = serializers.CharField()
    date = serializers.DateField()
