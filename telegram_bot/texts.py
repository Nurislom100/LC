"""Bot matnlari: uz / ru / en. `t(lang, key, **kwargs)` orqali ishlatiladi."""
import html

DEFAULT_LANG = "uz"

MONTHS = {
    "uz": ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust",
           "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"],
    "ru": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
           "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}

DAYS = {
    "uz": {"mo": "Du", "tu": "Se", "we": "Chor", "th": "Pay", "fr": "Ju", "sa": "Shan", "su": "Yak"},
    "ru": {"mo": "Пн", "tu": "Вт", "we": "Ср", "th": "Чт", "fr": "Пт", "sa": "Сб", "su": "Вс"},
    "en": {"mo": "Mon", "tu": "Tue", "we": "Wed", "th": "Thu", "fr": "Fri", "sa": "Sat", "su": "Sun"},
}


def fmt_days(value, lang):
    """'mo we fri' -> 'Du · Chor · Ju'"""
    table = DAYS.get(lang, DAYS[DEFAULT_LANG])
    # CRM'da "mo we fri" / "tu thu sa" ko'rinishida; birinchi 2 harfi bo'yicha moslashtiramiz
    return " · ".join(table.get(tok[:2], tok) for tok in (value or "").lower().split()) or "—"


def month_label(month_date, lang):
    return f"{MONTHS[lang][month_date.month - 1]} {month_date.year}"


TEXTS = {
    "choose_lang": {
        "uz": "🌐 Tilni tanlang / Выберите язык / Choose your language",
        "ru": "🌐 Tilni tanlang / Выберите язык / Choose your language",
        "en": "🌐 Tilni tanlang / Выберите язык / Choose your language",
    },
    "ask_name": {
        "uz": "👤 Ismingizni kiriting (ism va familiya):",
        "ru": "👤 Введите ваше имя (имя и фамилия):",
        "en": "👤 Enter your name (first and last name):",
    },
    "bad_name": {
        "uz": "Iltimos, ismingizni to'g'ri kiriting (kamida 2 ta belgi).",
        "ru": "Пожалуйста, введите имя корректно (минимум 2 символа).",
        "en": "Please enter a valid name (at least 2 characters).",
    },
    "welcome": {
        "uz": "Xush kelibsiz, <b>{name}</b>! 👋\nKerakli bo'limni tanlang:",
        "ru": "Добро пожаловать, <b>{name}</b>! 👋\nВыберите нужный раздел:",
        "en": "Welcome, <b>{name}</b>! 👋\nChoose a section:",
    },
    "menu": {
        "uz": "Kerakli bo'limni tanlang:",
        "ru": "Выберите нужный раздел:",
        "en": "Choose a section:",
    },
    "btn_rate": {
        "uz": "⭐ O'qituvchini baholash",
        "ru": "⭐ Оценить преподавателя",
        "en": "⭐ Rate a teacher",
    },
    "btn_trial": {
        "uz": "📝 Sinov darsiga yozilish",
        "ru": "📝 Записаться на пробный урок",
        "en": "📝 Sign up for a trial lesson",
    },
    "btn_report": {
        "uz": "📊 Barcha o'qituvchilar",
        "ru": "📊 Все преподаватели",
        "en": "📊 All teachers",
    },
    "btn_lang": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Сменить язык",
        "en": "🌐 Change language",
    },
    "btn_back": {"uz": "⬅️ Orqaga", "ru": "⬅️ Назад", "en": "⬅️ Back"},
    "btn_contact": {
        "uz": "📱 Raqamni yuborish",
        "ru": "📱 Отправить номер",
        "en": "📱 Share my number",
    },
    "ask_contact": {
        "uz": "📱 Shaxsingizni tasdiqlash uchun pastdagi tugma orqali telefon raqamingizni yuboring.\n\nRaqamni qo'lda yozish qabul qilinmaydi.",
        "ru": "📱 Для подтверждения личности отправьте свой номер телефона кнопкой ниже.\n\nВвод номера вручную не принимается.",
        "en": "📱 To verify you, share your phone number using the button below.\n\nTyping the number manually is not accepted.",
    },
    "use_button": {
        "uz": "Iltimos, pastdagi «📱 Raqamni yuborish» tugmasidan foydalaning.",
        "ru": "Пожалуйста, воспользуйтесь кнопкой «📱 Отправить номер» ниже.",
        "en": "Please use the “📱 Share my number” button below.",
    },
    "contact_not_yours": {
        "uz": "❌ Faqat o'zingizning raqamingizni yuborishingiz mumkin.",
        "ru": "❌ Можно отправить только свой собственный номер.",
        "en": "❌ You can only share your own number.",
    },
    "phone_saved": {
        "uz": "✅ Raqam qabul qilindi.",
        "ru": "✅ Номер принят.",
        "en": "✅ Number received.",
    },
    "not_found": {
        "uz": "❌ Bu raqam o'quv markaz ma'lumotlarida topilmadi.\n\nAgar siz o'quvchi bo'lsangiz, administratorga murojaat qiling: raqamingiz markazda boshqacha kiritilgan bo'lishi mumkin.",
        "ru": "❌ Этот номер не найден в базе учебного центра.\n\nЕсли вы студент, обратитесь к администратору: возможно, в центре указан другой номер.",
        "en": "❌ This number was not found in the learning center's records.\n\nIf you are a student, please contact the administrator: a different number may be on file.",
    },
    "no_groups": {
        "uz": "Sizda hozircha baholash mumkin bo'lgan faol guruh yo'q.",
        "ru": "У вас пока нет активных групп для оценки.",
        "en": "You have no active groups to rate yet.",
    },
    "pick_group": {
        "uz": "Baholamoqchi bo'lgan guruhingizni tanlang:\n(✅ — bu oy baholangan)",
        "ru": "Выберите группу, преподавателя которой хотите оценить:\n(✅ — оценено в этом месяце)",
        "en": "Choose the group whose teacher you want to rate:\n(✅ — already rated this month)",
    },
    "group_card": {
        "uz": "📚 <b>{group}</b>\n📅 {days}\n⏰ {start}–{end}\n👨‍🏫 O'qituvchi: <b>{teacher}</b>\n\nO'qituvchini baholang (1 dan 5 gacha):",
        "ru": "📚 <b>{group}</b>\n📅 {days}\n⏰ {start}–{end}\n👨‍🏫 Преподаватель: <b>{teacher}</b>\n\nОцените преподавателя (от 1 до 5):",
        "en": "📚 <b>{group}</b>\n📅 {days}\n⏰ {start}–{end}\n👨‍🏫 Teacher: <b>{teacher}</b>\n\nRate the teacher (1 to 5):",
    },
    "already": {
        "uz": "⏳ Siz <b>{teacher}</b> ({group}) o'qituvchisini bu oy allaqachon baholagansiz.\nKeyingi oyda qayta urinib ko'ring.",
        "ru": "⏳ Вы уже оценивали преподавателя <b>{teacher}</b> ({group}) в этом месяце.\nПопробуйте снова в следующем месяце.",
        "en": "⏳ You have already rated <b>{teacher}</b> ({group}) this month.\nPlease try again next month.",
    },
    "already_alert": {
        "uz": "Bu oy allaqachon baholagansiz. Keyingi oyda qayta urinib ko'ring.",
        "ru": "Вы уже оценили в этом месяце. Попробуйте в следующем.",
        "en": "You already rated this month. Try again next month.",
    },
    "rated_ok": {
        "uz": "✅ Rahmat! Siz <b>{teacher}</b> ga {stars} ({n}/5) baho berdingiz.\nBahoingiz anonim tarzda qabul qilindi.",
        "ru": "✅ Спасибо! Вы поставили <b>{teacher}</b> оценку {stars} ({n}/5).\nВаша оценка принята анонимно.",
        "en": "✅ Thank you! You rated <b>{teacher}</b> {stars} ({n}/5).\nYour rating was recorded anonymously.",
    },
    "not_allowed": {
        "uz": "Bu guruhni baholash mumkin emas.",
        "ru": "Эту группу оценить нельзя.",
        "en": "This group cannot be rated.",
    },
    "mgr_rating": {
        "uz": "⭐ <b>Yangi baho</b>\n📚 {group} guruh o'quvchisi\n👨‍🏫 O'qituvchi: <b>{teacher}</b>\nBaho: {stars} ({n}/5)\n📅 {date}",
        "ru": "⭐ <b>Новая оценка</b>\n📚 Студент группы {group}\n👨‍🏫 Преподаватель: <b>{teacher}</b>\nОценка: {stars} ({n}/5)\n📅 {date}",
        "en": "⭐ <b>New rating</b>\n📚 A student of group {group}\n👨‍🏫 Teacher: <b>{teacher}</b>\nRating: {stars} ({n}/5)\n📅 {date}",
    },
    "manager_only": {
        "uz": "Bu bo'lim faqat menejerlar uchun.",
        "ru": "Этот раздел доступен только менеджерам.",
        "en": "This section is for managers only.",
    },
    "report_title": {
        "uz": "📊 <b>O'qituvchilar reytingi</b>\n🗓 {period}\n",
        "ru": "📊 <b>Рейтинг преподавателей</b>\n🗓 {period}\n",
        "en": "📊 <b>Teacher ratings</b>\n🗓 {period}\n",
    },
    "report_row": {
        "uz": "{i}. <b>{teacher}</b> — {avg} ⭐ ({cnt} ta baho)",
        "ru": "{i}. <b>{teacher}</b> — {avg} ⭐ (оценок: {cnt})",
        "en": "{i}. <b>{teacher}</b> — {avg} ⭐ (ratings: {cnt})",
    },
    "report_none": {
        "uz": "{teacher} — baho yo'q",
        "ru": "{teacher} — нет оценок",
        "en": "{teacher} — no ratings",
    },
    "report_empty": {
        "uz": "Hozircha ma'lumot yo'q.",
        "ru": "Данных пока нет.",
        "en": "No data yet.",
    },
    "period_month": {"uz": "Shu oy", "ru": "Этот месяц", "en": "This month"},
    "period_prev": {"uz": "O'tgan oy", "ru": "Прошлый месяц", "en": "Last month"},
    "period_all": {"uz": "Hammasi", "ru": "Всё время", "en": "All time"},
    "period_all_label": {"uz": "Barcha vaqt", "ru": "Всё время", "en": "All time"},
    "mgr_linked": {
        "uz": "✅ Siz menejer sifatida ulandingiz. Endi yangi baholar shu yerga keladi.",
        "ru": "✅ Вы подключены как менеджер. Новые оценки будут приходить сюда.",
        "en": "✅ You are connected as a manager. New ratings will be sent here.",
    },
    "mgr_bad_link": {
        "uz": "❌ Menejer havolasi yaroqsiz yoki muddati o'tgan. Administratordan yangisini so'rang.",
        "ru": "❌ Ссылка менеджера недействительна или устарела. Попросите новую у администратора.",
        "en": "❌ The manager link is invalid or expired. Ask the administrator for a new one.",
    },
    "trial_ask_birth": {
        "uz": "🎂 Tug'ilgan sanangizni kiriting (KK.OO.YYYY, masalan 15.03.2008):",
        "ru": "🎂 Введите дату рождения (ДД.ММ.ГГГГ, например 15.03.2008):",
        "en": "🎂 Enter your date of birth (DD.MM.YYYY, e.g. 15.03.2008):",
    },
    "trial_bad_birth": {
        "uz": "Sana noto'g'ri. Iltimos, KK.OO.YYYY ko'rinishida kiriting (masalan 15.03.2008).",
        "ru": "Неверная дата. Введите в формате ДД.ММ.ГГГГ (например 15.03.2008).",
        "en": "Invalid date. Please use DD.MM.YYYY (e.g. 15.03.2008).",
    },
    "trial_pick_course": {
        "uz": "Qaysi kursga qiziqasiz?",
        "ru": "Какой курс вас интересует?",
        "en": "Which course are you interested in?",
    },
    "trial_ok": {
        "uz": "✅ So'rovingiz qabul qilindi! Tez orada administrator siz bilan bog'lanadi.",
        "ru": "✅ Ваша заявка принята! Администратор скоро свяжется с вами.",
        "en": "✅ Your request has been received! The administrator will contact you soon.",
    },
    "trial_dup": {
        "uz": "Sizning so'rovingiz allaqachon qabul qilingan. Administrator tez orada bog'lanadi.",
        "ru": "Ваша заявка уже принята. Администратор скоро свяжется с вами.",
        "en": "Your request has already been received. The administrator will contact you soon.",
    },
    "mgr_trial": {
        "uz": "📝 <b>Sinov darsiga yangi so'rov</b>\n👤 {name}\n📞 {phone}\n📚 Kurs: {course}\n🎂 {birth}\n📅 {date}",
        "ru": "📝 <b>Новая заявка на пробный урок</b>\n👤 {name}\n📞 {phone}\n📚 Курс: {course}\n🎂 {birth}\n📅 {date}",
        "en": "📝 <b>New trial lesson request</b>\n👤 {name}\n📞 {phone}\n📚 Course: {course}\n🎂 {birth}\n📅 {date}",
    },
    "any_course": {"uz": "Ko'rsatilmagan", "ru": "Не указан", "en": "Not specified"},
    "session_expired": {
        "uz": "Sessiya tugadi. Iltimos, qaytadan boshlang: /start",
        "ru": "Сессия истекла. Пожалуйста, начните заново: /start",
        "en": "Session expired. Please start again: /start",
    },
}


def t(lang, key, **kwargs):
    """Matnni oladi va HTML-xavfsiz tarzda formatlaydi (foydalanuvchi kiritgan qiymatlar escape qilinadi)."""
    lang = lang if lang in ("uz", "ru", "en") else DEFAULT_LANG
    safe = {k: html.escape(v) if isinstance(v, str) else v for k, v in kwargs.items()}
    return TEXTS[key][lang].format(**safe)
