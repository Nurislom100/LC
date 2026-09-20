from django.contrib import admin

from .models import BotUser, ManagerInvite, TeacherRating


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "telegram_id", "language", "is_manager", "created_at")
    list_filter = ("is_manager", "language")
    search_fields = ("full_name", "telegram_id")


@admin.register(ManagerInvite)
class ManagerInviteAdmin(admin.ModelAdmin):
    list_display = ("token", "created_by", "created_at", "expires_at", "used_at")


@admin.register(TeacherRating)
class TeacherRatingAdmin(admin.ModelAdmin):
    """Anonimlik: voter_hash admin'da ham ko'rsatilmaydi va o'zgartirilmaydi."""

    list_display = ("teacher", "group", "stars", "month")
    list_filter = ("month", "teacher")
    exclude = ("voter_hash",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
