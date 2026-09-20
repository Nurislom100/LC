"""
Bot uchun biznes-mantiq (sinxron, Django ORM). Botdan `sync_to_async` orqali chaqiriladi.
Hech qayerda "o'quvchi ismi -> baho" bog'lanishi ko'rsatilmaydi (anonimlik).
"""
import hashlib
import hmac
import re
from datetime import timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count, F, Q, Value
from django.db.models.functions import Replace
from django.utils import timezone

from common.models import Course, Lead, Student, Teacher

from .models import BotUser, ManagerInvite, TeacherRating

# CRM'da yangi so'rov (Lead) uchun ishlatiladigan status qiymati.
# Lead.status_choices ning birinchisi "Request". Agar bazangizda boshqacha
# yozilgan bo'lsa (masalan tarjima qilingan), shu yerda o'zgartiring.
LEAD_STATUS_NEW = "Request"
ACTIVE = "Active"


# ---------------------------------------------------------------- vaqt
def bot_tz():
    return ZoneInfo(getattr(settings, "BOT_TIMEZONE", "Asia/Tashkent"))


def local_today():
    return timezone.now().astimezone(bot_tz()).date()


def current_month():
    return local_today().replace(day=1)


def previous_month():
    return (current_month() - timedelta(days=1)).replace(day=1)


# ---------------------------------------------------------------- telefon
def last9(phone):
    """'+998 90 123-45-67' -> '901234567'"""
    return re.sub(r"\D", "", phone or "")[-9:]


def normalize_phone(phone):
    digits = re.sub(r"\D", "", phone or "")
    return f"+{digits}" if digits else ""


def _clean_phone_expr(field="phone"):
    """Bazadagi raqamdan bo'sh joy, chiziqcha, qavs va + belgilarini olib tashlaydi."""
    expr = F(field)
    for ch in (" ", "-", "+", "(", ")", "."):
        expr = Replace(expr, Value(ch), Value(""))
    return expr


def students_by_phone(phone):
    key = last9(phone)
    if len(key) < 9:
        return Student.objects.none()
    return (
        Student.objects.annotate(clean_phone=_clean_phone_expr())
        .filter(clean_phone__endswith=key, status=ACTIVE)
    )


# ---------------------------------------------------------------- foydalanuvchi
def voter_hash(telegram_id):
    return hmac.new(
        settings.SECRET_KEY.encode(), f"rating:{telegram_id}".encode(), hashlib.sha256
    ).hexdigest()


def get_bot_user(telegram_id):
    return BotUser.objects.filter(telegram_id=telegram_id).first()


def get_or_create_bot_user(telegram_id):
    user, _ = BotUser.objects.get_or_create(telegram_id=telegram_id)
    return user


def set_language(telegram_id, lang):
    BotUser.objects.filter(telegram_id=telegram_id).update(language=lang)
    return get_bot_user(telegram_id)


def set_name(telegram_id, name):
    BotUser.objects.filter(telegram_id=telegram_id).update(full_name=name.strip()[:255])
    return get_bot_user(telegram_id)


def save_phone(telegram_id, phone):
    BotUser.objects.filter(telegram_id=telegram_id).update(phone=normalize_phone(phone))
    return get_bot_user(telegram_id)


# ---------------------------------------------------------------- menejer
def create_manager_invite(crm_user):
    return ManagerInvite.objects.create(created_by=crm_user)


def active_invites():
    return [i for i in ManagerInvite.objects.filter(used_at__isnull=True, expires_at__gt=timezone.now())]


@transaction.atomic
def consume_manager_invite(token, telegram_id, default_name=""):
    """Bir martalik havolani ishlatadi. True - muvaffaqiyatli."""
    invite = ManagerInvite.objects.select_for_update().filter(token=token).first()
    if not invite or not invite.is_active:
        return False
    user, _ = BotUser.objects.get_or_create(telegram_id=telegram_id)
    user.is_manager = True
    if not user.full_name and default_name:
        user.full_name = default_name[:255]
    user.save()
    invite.used_by = user
    invite.used_at = timezone.now()
    invite.save()
    return True


def manager_targets():
    return list(BotUser.objects.filter(is_manager=True).values_list("telegram_id", "language"))


# ---------------------------------------------------------------- baholash
def rateable_groups(bot_user):
    """
    Qaytaradi: (topildimi, [guruhlar]).
    Raqam bo'yicha CRM'dagi FAOL o'quvchi yozuvlari topiladi (har bir yozuv = bitta guruh).
    """
    students = (
        students_by_phone(bot_user.phone)
        .filter(group__status=ACTIVE, group__teacher__isnull=False)
        .select_related("group", "group__teacher")
    )
    found = students_by_phone(bot_user.phone).exists()

    rated = set(
        TeacherRating.objects.filter(voter_hash=voter_hash(bot_user.telegram_id), month=current_month())
        .values_list("group_id", "teacher_id")
    )
    result, seen = [], set()
    for s in students:
        g = s.group
        if g.id in seen:
            continue
        seen.add(g.id)
        result.append(
            {
                "group_id": g.id,
                "title": g.title,
                "teacher_id": g.teacher_id,
                "teacher": g.teacher.full_name,
                "days": g.lesson_days,
                "start": g.start_time.strftime("%H:%M"),
                "end": g.end_time.strftime("%H:%M"),
                "rated": (g.id, g.teacher_id) in rated,
            }
        )
    result.sort(key=lambda x: x["title"].lower())
    return found, result


def group_for_rating(bot_user, group_id):
    _, groups = rateable_groups(bot_user)
    return next((g for g in groups if g["group_id"] == group_id), None)


def submit_rating(bot_user, group_id, stars):
    """('ok'|'already'|'not_allowed'|'invalid', info)"""
    if stars not in (1, 2, 3, 4, 5):
        return "invalid", None
    info = group_for_rating(bot_user, group_id)
    if not info:
        return "not_allowed", None
    if info["rated"]:
        return "already", info
    try:
        with transaction.atomic():
            TeacherRating.objects.create(
                group_id=info["group_id"],
                teacher_id=info["teacher_id"],
                voter_hash=voter_hash(bot_user.telegram_id),
                stars=stars,
                month=current_month(),
            )
    except IntegrityError:
        return "already", info
    return "ok", info


# ---------------------------------------------------------------- hisobot
def teacher_report(period):
    """period: 'month' | 'prev' | 'all'. Qaytaradi (oy yoki None, [qatorlar])."""
    qs = TeacherRating.objects.all()
    month = None
    if period == "month":
        month = current_month()
        qs = qs.filter(month=month)
    elif period == "prev":
        month = previous_month()
        qs = qs.filter(month=month)

    agg = {
        r["teacher_id"]: r
        for r in qs.values("teacher_id").annotate(avg=Avg("stars"), cnt=Count("id"))
    }
    teachers = Teacher.objects.filter(Q(status=ACTIVE) | Q(id__in=list(agg.keys())))

    rows = []
    for tch in teachers:
        a = agg.get(tch.id)
        rows.append(
            {
                "teacher": tch.full_name,
                "avg": round(float(a["avg"]), 2) if a else None,
                "cnt": a["cnt"] if a else 0,
            }
        )
    rows.sort(key=lambda r: (r["avg"] is None, -(r["avg"] or 0), -r["cnt"], r["teacher"].lower()))
    return month, rows


# ---------------------------------------------------------------- sinov darsi (Lead)
def list_courses():
    return list(Course.objects.order_by("title").values("id", "title"))


def create_trial_lead(bot_user, birth_date, course_id):
    """('ok'|'duplicate', {'course': nomi})"""
    key = last9(bot_user.phone)
    dup = (
        Lead.objects.annotate(clean_phone=_clean_phone_expr())
        .filter(clean_phone__endswith=key, status=LEAD_STATUS_NEW)
        .exists()
    )
    if dup:
        return "duplicate", None
    course = Course.objects.filter(pk=course_id).first() if course_id else None
    Lead.objects.create(
        full_name=bot_user.full_name,
        birth_date=birth_date,
        phone=bot_user.phone,
        address="Telegram bot",
        interested_course=course,
        status=LEAD_STATUS_NEW,
    )
    return "ok", {"course": course.title if course else ""}
