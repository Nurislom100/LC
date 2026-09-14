from django import forms

from .models import PaymentReceipt, Subscription


class ReceiptUploadForm(forms.ModelForm):
    class Meta:
        model = PaymentReceipt
        fields = ['receipt_image']
        widgets = {
            'receipt_image': forms.ClearableFileInput(attrs={'accept': 'image/*'})
        }


class SubscriptionEditForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['billing_enabled', 'price_per_student', 'card_number', 'card_holder_name', 'payment_day']