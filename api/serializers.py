from rest_framework import serializers
from sales.models import Sales

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
