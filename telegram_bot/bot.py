"""
Telegram bot (aiogram 3). Django ORM bilan ishlash uchun barcha DB chaqiruvlari
`db(...)` orqali (sync_to_async) bajariladi.

Ishga tushirish:  python manage.py runbot
"""
import logging
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db import close_old_connections

from . import services
from .texts import fmt_days, month_label, t

log = logging.getLogger(__name__)
router = Router()


# ------------------------------------------------------------------ yordamchilar
def _wrap(func):
    def inner(*args, **kwargs):
        close_old_connections()  # uzoq ishlaydigan jarayonda "uzilgan ulanish" xatosidan saqlaydi
        try:
            return func(*args, **kwargs)
        finally:
            close_old_connections()

    return inner


async def db(func, *args, **kwargs):
    return await sync_to_async(_wrap(func), thread_sensitive=True)(*args, **kwargs)


class Flow(StatesGroup):
    name = State()
    contact = State()
    birth = State()


def stars_text(n):
    return "⭐" * n


def lang_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            ]
        ]
    )


def menu_kb(user):
    lang = user.lang
    rows = [
        [InlineKeyboardButton(text=t(lang, "btn_rate"), callback_data="menu:rate")],
        [InlineKeyboardButton(text=t(lang, "btn_trial"), callback_data="menu:trial")],
    ]
    if user.is_manager:
        rows.append([InlineKeyboardButton(text=t(lang, "btn_report"), callback_data="menu:report")])
    rows.append([InlineKeyboardButton(text=t(lang, "btn_lang"), callback_data="menu:lang")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def contact_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, "btn_contact"), request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def show_menu(message: Message, user, greeting=False):
    key = "welcome" if greeting else "menu"
    await message.answer(t(user.lang, key, name=user.full_name), reply_markup=menu_kb(user))


async def get_registered(event):
    """Ro'yxatdan o'tgan foydalanuvchini qaytaradi, aks holda /start ga yo'naltiradi."""
    tg_id = event.from_user.id
    user = await db(services.get_bot_user, tg_id)
    if user and user.is_registered:
        return user
    msg = event.message if isinstance(event, CallbackQuery) else event
    await msg.answer(t("uz", "choose_lang"), reply_markup=lang_kb())
    return None


async def send_safe(bot: Bot, chat_id, text):
    try:
        await bot.send_message(chat_id, text)
    except (TelegramForbiddenError, TelegramBadRequest) as exc:
        log.warning("Xabar yuborilmadi (%s): %s", chat_id, exc)


async def notify_managers(bot: Bot, build_text):
    """build_text(lang) -> matn. Har bir menejerga o'z tilida yuboriladi."""
    for chat_id, lang in await db(services.manager_targets):
        await send_safe(bot, chat_id, build_text(lang or "uz"))


# ------------------------------------------------------------------ /start, til, ism
@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    arg = (command.args or "").strip()
    user = await db(services.get_or_create_bot_user, message.from_user.id)

    if arg.startswith("mgr_"):
        ok = await db(
            services.consume_manager_invite, arg[4:], message.from_user.id, message.from_user.first_name or ""
        )
        user = await db(services.get_bot_user, message.from_user.id)
        await message.answer(t(user.lang, "mgr_linked" if ok else "mgr_bad_link"))

    if user.is_registered:
        await show_menu(message, user, greeting=True)
    else:
        await message.answer(t("uz", "choose_lang"), reply_markup=lang_kb())


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    user = await get_registered(message)
    if user:
        await show_menu(message, user)


@router.callback_query(F.data.startswith("lang:"))
async def pick_lang(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    lang = cb.data.split(":")[1]
    if lang not in ("uz", "ru", "en"):
        return
    await db(services.get_or_create_bot_user, cb.from_user.id)
    user = await db(services.set_language, cb.from_user.id, lang)
    if user.full_name:
        await show_menu(cb.message, user, greeting=True)
    else:
        await state.set_state(Flow.name)
        await cb.message.answer(t(lang, "ask_name"))


@router.message(Flow.name, F.text)
async def got_name(message: Message, state: FSMContext):
    name = (message.text or "").strip()
    user = await db(services.get_bot_user, message.from_user.id)
    if not user:
        return
    if len(name) < 2 or len(name) > 100 or name.startswith("/"):
        await message.answer(t(user.lang, "bad_name"))
        return
    user = await db(services.set_name, message.from_user.id, name)
    await state.clear()
    await show_menu(message, user, greeting=True)


# ------------------------------------------------------------------ menyu
@router.callback_query(F.data == "menu:lang")
async def menu_lang(cb: CallbackQuery):
    await cb.answer()
    await cb.message.answer(t("uz", "choose_lang"), reply_markup=lang_kb())


@router.callback_query(F.data == "menu:rate")
async def menu_rate(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user = await get_registered(cb)
    if not user:
        return
    if not user.phone:
        await state.set_state(Flow.contact)
        await state.update_data(purpose="rate")
        await cb.message.answer(t(user.lang, "ask_contact"), reply_markup=contact_kb(user.lang))
        return
    await show_groups(cb.message, user)


@router.callback_query(F.data == "menu:trial")
async def menu_trial(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user = await get_registered(cb)
    if not user:
        return
    if not user.phone:
        await state.set_state(Flow.contact)
        await state.update_data(purpose="trial")
        await cb.message.answer(t(user.lang, "ask_contact"), reply_markup=contact_kb(user.lang))
        return
    await state.set_state(Flow.birth)
    await cb.message.answer(t(user.lang, "trial_ask_birth"))


# ------------------------------------------------------------------ kontakt tekshiruvi
@router.message(Flow.contact, F.contact)
async def got_contact(message: Message, state: FSMContext):
    user = await get_registered(message)
    if not user:
        return
    contact = message.contact
    # Faqat o'zining kontakti qabul qilinadi (boshqa odamning raqamini yuborib bo'lmaydi)
    if contact.user_id != message.from_user.id:
        await message.answer(t(user.lang, "contact_not_yours"), reply_markup=contact_kb(user.lang))
        return

    purpose = (await state.get_data()).get("purpose")
    user = await db(services.save_phone, message.from_user.id, contact.phone_number)
    await state.clear()
    await message.answer(t(user.lang, "phone_saved"), reply_markup=ReplyKeyboardRemove())

    if purpose == "trial":
        await state.set_state(Flow.birth)
        await message.answer(t(user.lang, "trial_ask_birth"))
    else:
        await show_groups(message, user)


@router.message(Flow.contact)
async def contact_expected(message: Message):
    user = await get_registered(message)
    if user:
        await message.answer(t(user.lang, "use_button"), reply_markup=contact_kb(user.lang))


# ------------------------------------------------------------------ baholash
async def show_groups(message: Message, user, edit=False):
    found, groups = await db(services.rateable_groups, user)
    if not found:
        await message.answer(t(user.lang, "not_found"), reply_markup=menu_kb(user))
        return
    if not groups:
        await message.answer(t(user.lang, "no_groups"), reply_markup=menu_kb(user))
        return
    rows = [
        [
            InlineKeyboardButton(
                text=f"{'✅ ' if g['rated'] else ''}{g['title']} — {g['teacher']}"[:60],
                callback_data=f"grp:{g['group_id']}",
            )
        ]
        for g in groups
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    text = t(user.lang, "pick_group")
    if edit:
        try:
            await message.edit_text(text, reply_markup=kb)
            return
        except TelegramBadRequest:
            pass
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "back:groups")
async def back_groups(cb: CallbackQuery):
    await cb.answer()
    user = await get_registered(cb)
    if user:
        await show_groups(cb.message, user, edit=True)


@router.callback_query(F.data.regexp(r"^grp:(\d+)$"))
async def pick_group(cb: CallbackQuery):
    user = await get_registered(cb)
    if not user:
        await cb.answer()
        return
    gid = int(cb.data.split(":")[1])
    info = await db(services.group_for_rating, user, gid)
    if not info:
        await cb.answer(t(user.lang, "not_allowed"), show_alert=True)
        return
    if info["rated"]:
        await cb.answer(t(user.lang, "already_alert"), show_alert=True)
        return
    await cb.answer()

    today = services.local_today().strftime("%d.%m.%Y")
    stars_row = [
        InlineKeyboardButton(text=f"{n}⭐", callback_data=f"rate:{gid}:{n}") for n in range(1, 6)
    ]
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            stars_row,
            [InlineKeyboardButton(text=t(user.lang, "btn_back"), callback_data="back:groups")],
            [InlineKeyboardButton(text=f"📅 {today}", callback_data="noop")],  # eng pastda bugungi sana
        ]
    )
    text = t(
        user.lang,
        "group_card",
        group=info["title"],
        days=fmt_days(info["days"], user.lang),
        start=info["start"],
        end=info["end"],
        teacher=info["teacher"],
    )
    try:
        await cb.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        await cb.message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "noop")
async def noop(cb: CallbackQuery):
    await cb.answer()


@router.callback_query(F.data.regexp(r"^rate:(\d+):([1-5])$"))
async def do_rate(cb: CallbackQuery):
    user = await get_registered(cb)
    if not user:
        await cb.answer()
        return
    _, gid, stars = cb.data.split(":")
    gid, stars = int(gid), int(stars)
    status, info = await db(services.submit_rating, user, gid, stars)

    if status == "not_allowed" or status == "invalid":
        await cb.answer(t(user.lang, "not_allowed"), show_alert=True)
        return
    await cb.answer()

    back_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t(user.lang, "btn_back"), callback_data="back:groups")]]
    )
    if status == "already":
        text = t(user.lang, "already", teacher=info["teacher"], group=info["title"])
    else:
        text = t(user.lang, "rated_ok", teacher=info["teacher"], stars=stars_text(stars), n=stars)
        today = services.local_today().strftime("%d.%m.%Y")
        # Menejerga: guruh nomi, o'qituvchi, baho, sana. O'quvchi ismi YUBORILMAYDI.
        await notify_managers(
            cb.bot,
            lambda lang: t(
                lang, "mgr_rating",
                group=info["title"], teacher=info["teacher"], stars=stars_text(stars), n=stars, date=today,
            ),
        )
    try:
        await cb.message.edit_text(text, reply_markup=back_kb)
    except TelegramBadRequest:
        await cb.message.answer(text, reply_markup=back_kb)


# ------------------------------------------------------------------ sinov darsi
def parse_birth(text):
    raw = (text or "").strip().replace("/", ".").replace("-", ".").replace(" ", ".")
    try:
        d = datetime.strptime(raw, "%d.%m.%Y").date()
    except ValueError:
        return None
    age = (services.local_today() - d).days / 365.25
    return d if 3 <= age <= 90 else None


@router.message(Flow.birth, F.text)
async def got_birth(message: Message, state: FSMContext):
    user = await get_registered(message)
    if not user:
        return
    birth = parse_birth(message.text)
    if not birth:
        await message.answer(t(user.lang, "trial_bad_birth"))
        return
    await state.update_data(birth=birth.isoformat())

    courses = await db(services.list_courses)
    if not courses:
        await finish_trial(message, state, user, None)
        return
    rows = [[InlineKeyboardButton(text=c["title"][:60], callback_data=f"course:{c['id']}")] for c in courses]
    await message.answer(t(user.lang, "trial_pick_course"), reply_markup=InlineKeyboardMarkup(inline_keyboard=rows))


@router.callback_query(F.data.regexp(r"^course:(\d+)$"))
async def pick_course(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user = await get_registered(cb)
    if not user:
        return
    if not (await state.get_data()).get("birth"):
        await cb.message.answer(t(user.lang, "session_expired"))
        return
    await finish_trial(cb.message, state, user, int(cb.data.split(":")[1]))


async def finish_trial(message: Message, state: FSMContext, user, course_id):
    birth = datetime.fromisoformat((await state.get_data())["birth"]).date()
    await state.clear()
    status, info = await db(services.create_trial_lead, user, birth, course_id)
    if status == "duplicate":
        await message.answer(t(user.lang, "trial_dup"), reply_markup=menu_kb(user))
        return
    await message.answer(t(user.lang, "trial_ok"), reply_markup=menu_kb(user))
    today = services.local_today().strftime("%d.%m.%Y")
    await notify_managers(
        message.bot,
        lambda lang: t(
            lang, "mgr_trial",
            name=user.full_name, phone=user.phone,
            course=info["course"] or t(lang, "any_course"),
            birth=birth.strftime("%d.%m.%Y"), date=today,
        ),
    )


# ------------------------------------------------------------------ menejer hisoboti
def report_kb(lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "period_month"), callback_data="rep:month"),
                InlineKeyboardButton(text=t(lang, "period_prev"), callback_data="rep:prev"),
                InlineKeyboardButton(text=t(lang, "period_all"), callback_data="rep:all"),
            ]
        ]
    )


async def build_report(lang, period):
    month, rows = await db(services.teacher_report, period)
    label = month_label(month, lang) if month else t(lang, "period_all_label")
    lines = [t(lang, "report_title", period=label)]
    if not rows:
        lines.append(t(lang, "report_empty"))
    n = 0
    for r in rows:
        if r["avg"] is None:
            lines.append("▫️ " + t(lang, "report_none", teacher=r["teacher"]))
        else:
            n += 1
            lines.append(t(lang, "report_row", i=n, teacher=r["teacher"], avg=r["avg"], cnt=r["cnt"]))
    return "\n".join(lines)


def chunk_text(text, limit=3900):
    chunks, cur = [], ""
    for line in text.split("\n"):
        if len(cur) + len(line) + 1 > limit:
            chunks.append(cur)
            cur = ""
        cur += line + "\n"
    if cur.strip():
        chunks.append(cur)
    return chunks


async def send_report(message: Message, user, period, edit=False):
    text = await build_report(user.lang, period)
    chunks = chunk_text(text)
    if edit and len(chunks) == 1:
        try:
            await message.edit_text(chunks[0], reply_markup=report_kb(user.lang))
            return
        except TelegramBadRequest:  # xabar o'zgarmagan bo'lsa
            return
    for i, part in enumerate(chunks):
        last = i == len(chunks) - 1
        await message.answer(part, reply_markup=report_kb(user.lang) if last else None)


@router.message(Command("all_teachers"))
async def cmd_all_teachers(message: Message):
    user = await get_registered(message)
    if not user:
        return
    if not user.is_manager:
        await message.answer(t(user.lang, "manager_only"))
        return
    await send_report(message, user, "month")


@router.callback_query(F.data == "menu:report")
async def menu_report(cb: CallbackQuery):
    await cb.answer()
    user = await get_registered(cb)
    if not user:
        return
    if not user.is_manager:
        await cb.message.answer(t(user.lang, "manager_only"))
        return
    await send_report(cb.message, user, "month")


@router.callback_query(F.data.regexp(r"^rep:(month|prev|all)$"))
async def report_period(cb: CallbackQuery):
    await cb.answer()
    user = await get_registered(cb)
    if not user or not user.is_manager:
        return
    await send_report(cb.message, user, cb.data.split(":")[1], edit=True)


# ------------------------------------------------------------------ boshqa xabarlar
@router.message()
async def fallback(message: Message):
    user = await get_registered(message)
    if user:
        await show_menu(message, user)


# ------------------------------------------------------------------ ishga tushirish
def build_dispatcher():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    return dp


async def main():
    token = getattr(settings, "BOT_TOKEN", "")
    if not token:
        raise RuntimeError("BOT_TOKEN o'rnatilmagan (environment o'zgaruvchisi).")
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = build_dispatcher()
    await bot.set_my_commands(
        [BotCommand(command="start", description="Start / Начать"),
         BotCommand(command="menu", description="Menu / Меню")]
    )
    log.info("Bot ishga tushdi")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
