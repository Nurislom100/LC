from django.shortcuts import redirect
from django.urls import reverse

from .models import Subscription

# Bu manzillar HAR DOIM ochiq qoladi - aks holda "to'lov" sahifasining
# o'ziga ham kirib bo'lmay qoladi (cheksiz redirect loop bo'ladi).
EXEMPT_PREFIXES = [
    '/billing/',
    '/static/',
    '/media/',
    '/admin/',       # Django admin
    '/sign-in/',
    '/sign-out/',
    '/i18n/',
]


class SubscriptionGateMiddleware:
    """
    Har bir so'rovda obuna holatini tekshiradi. Agar to'lov muddati
    o'tgan bo'lsa (superuser bo'lmagan foydalanuvchilar uchun), so'ralgan
    sahifa nima bo'lishidan qat'iy nazar, "to'lov" sahifasiga yo'naltiradi.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if any(path.startswith(p) for p in EXEMPT_PREFIXES):
            return self.get_response(request)

        user = getattr(request, 'user', None)

        # Anonim (login qilmagan) foydalanuvchilar - login sahifasiga
        # borishga ruxsat, alohida auth middleware o'zi hal qiladi.
        if not user or not user.is_authenticated:
            return self.get_response(request)

        # Superuser - obuna holatidan qat'iy nazar bloklanmaydi
        # (aks holda superadmin ham o'z panelidan boshqa hech narsaga
        # kira olmay qolishi mumkin).
        if user.is_superuser:
            return self.get_response(request)

        subscription = Subscription.get_solo()
        if subscription.is_overdue():
            return redirect(reverse('billing:status'))

        return self.get_response(request)