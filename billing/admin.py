from django.contrib import admin
from .models import Subscription, PaymentReceipt


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['price_per_student', 'card_number', 'payment_day', 'next_due_date']


@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'uploaded_by', 'uploaded_at']
    list_filter = ['status']