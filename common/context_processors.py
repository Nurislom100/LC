# manager/context_processors.py (yoki mos app nomi)
from .models import *  # Markaz ma'lumotlari modeli nomi


def center_info(request):
    info = Informations.objects.first()
    return {
        'center_info': info
    }