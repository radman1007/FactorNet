# serializers.py
from rest_framework import serializers
from .models import Customer, Invoice, InvoiceItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_id', 'invoice_number', 'created_at', 'due_date',
            'discount', 'tax_percent', 'notes', 'status', 'customer', 'customer_id', 'items'
        ]