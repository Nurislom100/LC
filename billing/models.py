import calendar
from datetime import date

from django.conf import settings
from django.db import models
from django.utils import timezone


def add_one_month_same_day(d: date, day: int) -> date:
    """Berilgan kundan keyingi oyning `day`-sanasini qaytaradi.
    Agar oyda shuncha kun bo'lmasa (masalan fevralda 31), oyning oxirgi kuni olinadi."""
    year = d.year
    month = d.month + 1
    if month > 12:
        month = 1
        year += 1
    last_day_of_month = calendar.monthrange(year, month)[1]
    safe_day = min(day, last_day_of_month)
    return date(year, month, safe_day)


class Subscription(models.Model):
    """
    Bitta o'quv markaz = bitta serverga o'rnatilgan loyiha bo'lgani uchun
    bu jadvalda har doim FAQAT BITTA yozuv bo'ladi (singleton).
    Tahrirlash faqat superuser orqali (billing:admin-panel view'ida) amalga oshadi.
    """
    billing_enabled = models.BooleanField(
        default=True,
        verbose_name="Oylik to'lov tizimi yoqilganmi",
        help_text="O'chirilsa - markaz platformani to'liq sotib olgan hisoblanadi, hech qachon bloklanmaydi."
    )
    price_per_student = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        verbose_name="Bir o'quvchidan olinadigan summa"
    )
    card_number = models.CharField(
        max_length=32, blank=True, default="",
        verbose_name="To'lov qabul qilinadigan karta raqami"
    )
    card_holder_name = models.CharField(
        max_length=64, blank=True, default="",
        verbose_name="Karta egasi (ixtiyoriy)"
    )
    payment_day = models.PositiveSmallIntegerField(
        default=15,
        verbose_name="Har oyning nechanchi kuni to'lov qilinishi kerak"
    )
    last_payment_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Obuna sozlamalari"
        verbose_name_plural = "Obuna sozlamalari"

    def __str__(self):
        return "Obuna sozlamalari"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        return obj

    def get_student_count(self):
        """O'quvchilar sonini bazadan REAL VAQTDA hisoblaydi.
        Alohida saqlanadigan son emas - shu bilan qo'shilgan/o'chirilgan
        o'quvchilar avtomatik hisobga kirib/chiqib turadi."""
        # Loyihada Student modeli boshqa ilovada (masalan common yoki manager)
        # bo'lgani uchun import xatoligining oldini olish uchun shu yerda import qilinadi.
        from common.models import Student
        return Student.objects.count()

    def get_total_amount(self):
        return self.get_student_count() * self.price_per_student

    def is_configured(self):
        """Superadmin hali sozlamalarni umuman kiritmagan bo'lsa (masalan
        birinchi marta deploy qilingan bo'lsa), bloklamaymiz - aks holda
        hech kim hech narsa qila olmay qoladi."""
        return bool(self.card_number) and self.price_per_student > 0

    def is_overdue(self):
        if not self.billing_enabled:
            return False
        if not self.is_configured():
            return False
        if not self.next_due_date:
            return False
        return timezone.now().date() > self.next_due_date

    def mark_paid(self, payment_date=None):
        """To'lov superadmin tomonidan tasdiqlanganda chaqiriladi."""
        today = payment_date or timezone.now().date()
        self.last_payment_date = today
        base = self.next_due_date if self.next_due_date and self.next_due_date >= today else today
        self.next_due_date = add_one_month_same_day(base, self.payment_day)
        self.save()


class PaymentReceipt(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, "Kutilmoqda"),
        (STATUS_APPROVED, "Tasdiqlangan"),
        (STATUS_REJECTED, "Rad etilgan"),
    ]

    receipt_image = models.ImageField(upload_to='billing_receipts/%Y/%m/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='uploaded_receipts'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='reviewed_receipts'
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "To'lov cheki"
        verbose_name_plural = "To'lov cheklari"

    def __str__(self):
        return f"Chek #{self.pk} ({self.get_status_display()})"