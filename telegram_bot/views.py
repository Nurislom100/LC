import base64
import io

import qrcode
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from . import services
from .models import BotUser, ManagerInvite


def _allowed(user):
    return user.is_superuser or getattr(user, "role", None) == "manager"


def _qr_base64(url):
    img = qrcode.make(url, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


@login_required
def bot_settings(request):
    """Menejer paneli: o'quvchilar havolasi + QR, menejer uchun bir martalik havolalar."""
    if not _allowed(request.user):
        return HttpResponseForbidden("Faqat menejer uchun.")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "new_invite":
            services.create_manager_invite(request.user)
        elif action == "cancel_invite":
            ManagerInvite.objects.filter(pk=request.POST.get("id"), used_at__isnull=True).delete()
        elif action == "remove_manager":
            get_object_or_404(BotUser, pk=request.POST.get("id"))
            BotUser.objects.filter(pk=request.POST.get("id")).update(is_manager=False)
        return redirect("telegram_bot:settings")

    username = getattr(settings, "BOT_USERNAME", "").lstrip("@")
    student_link = f"https://t.me/{username}" if username else ""
    invites = [
        {"obj": i, "link": f"https://t.me/{username}?start=mgr_{i.token}" if username else ""}
        for i in services.active_invites()
    ]
    return render(
        request,
        "telegram_bot/bot_settings.html",
        {
            "configured": bool(username and getattr(settings, "BOT_TOKEN", "")),
            "student_link": student_link,
            "qr": _qr_base64(student_link) if student_link else "",
            "invites": invites,
            "managers": BotUser.objects.filter(is_manager=True),
        },
    )
