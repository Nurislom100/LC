import secrets
from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class BotUser(models.Model):
    """Botga kirgan Telegram foydalanuvchisi (o'quvchi yoki menejer)."""

    LANG_CHOICES = [("uz", "O'zbekcha"), ("ru", "Русский"), ("en", "English")]

    telegram_id = models.BigIntegerField(unique=True)
    language = models.CharField(max_length=2, choices=LANG_CHOICES, blank=True, default="")
    full_name = models.CharField(max_length=255, blank=True)
    # Faqat Telegram "kontakt yuborish" tugmasi orqali (tasdiqlangan) raqam yoziladi
    phone = models.CharField(max_length=20, blank=True)
    is_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bot_users"

    def __str__(self):
        return f"{self.full_name or self.telegram_id} ({'manager' if self.is_manager else 'user'})"

    @property
    def lang(self):
        return self.language or "uz"

    @property
    def is_registered(self):
        return bool(self.language and self.full_name)


def _new_token():
    return secrets.token_urlsafe(12)


def _default_expiry():
    return timezone.now() + timedelta(hours=48)


class ManagerInvite(models.Model):
    """Menejer uchun bir martalik havola. Ishlatilgach yoki muddati o'tgach yaroqsiz."""

    token = models.CharField(max_length=64, unique=True, default=_new_token)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=_default_expiry)
    used_by = models.ForeignKey(BotUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "bot_manager_invites"
        ordering = ["-created_at"]

    @property
    def is_active(self):
        return self.used_at is None and self.expires_at > timezone.now()


class TeacherRating(models.Model):
    """
    O'quvchining o'qituvchiga bergan bahosi.

    ANONIMLIK: o'quvchiga to'g'ridan-to'g'ri havola YO'Q. Faqat `voter_hash`
    (telegram_id ning HMAC hashi) saqlanadi - u "oyiga bir marta" qoidasini
    tekshirish uchun kerak. Menejerga o'quvchi haqida hech narsa ko'rsatilmaydi.
    """

    group = models.ForeignKey("common.Group", on_delete=models.CASCADE, related_name="ratings")
    teacher = models.ForeignKey("common.Teacher", on_delete=models.CASCADE, related_name="ratings")
    voter_hash = models.CharField(max_length=64, db_index=True)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    month = models.DateField(help_text="Oyning 1-sanasi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "teacher_ratings"
        constraints = [
            models.UniqueConstraint(
                fields=["voter_hash", "group", "teacher", "month"],
                name="one_rating_per_voter_group_teacher_month",
            ),
            models.CheckConstraint(
                condition=models.Q(stars__gte=1, stars__lte=5),
                name="rating_stars_1_to_5",
            ),
        ]

    def __str__(self):
        return f"{self.teacher} - {self.stars}★ ({self.month:%Y-%m})"
