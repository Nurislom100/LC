# Create your views here.
import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ReceiptUploadForm, SubscriptionEditForm
from .models import Subscription, PaymentReceipt

ADMIN_SESSION_KEY = 'billing_admin_verified'


# ---------------------------------------------------------------------
# 1) BARCHA ROLLAR KO'RA OLADIGAN (faqat ko'rish) TO'LOV SAHIFASI
#    - to'lov muddati o'tganda avtomatik shu yerga tushiladi
#    - normal holatda ham istalgan vaqt ko'rish uchun kirish mumkin
# ---------------------------------------------------------------------
@login_required
def status_view(request):
    subscription = Subscription.get_solo()

    if request.method == 'POST':
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.uploaded_by = request.user
            receipt.save()
            return redirect('billing:status')
    else:
        form = ReceiptUploadForm()

    pending_receipt = PaymentReceipt.objects.filter(
        status=PaymentReceipt.STATUS_PENDING
    ).order_by('-uploaded_at').first()

    context = {
        'subscription': subscription,
        'student_count': subscription.get_student_count(),
        'total_amount': subscription.get_total_amount(),
        'is_overdue': subscription.is_overdue(),
        'form': form,
        'pending_receipt': pending_receipt,
    }
    return render(request, 'billing/status.html', context)


# ---------------------------------------------------------------------
# 2) SUPERADMIN LOGIN MODALI (AJAX)
#    Header'dagi tugma bosilganda chiqadigan kichik oynadan yuboriladi.
# ---------------------------------------------------------------------
@require_POST
def admin_login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        data = request.POST

    username = data.get('username', '')
    password = data.get('password', '')

    user = authenticate(request, username=username, password=password)

    if user is not None and user.is_superuser:
        request.session[ADMIN_SESSION_KEY] = True
        request.session.set_expiry(60 * 30)  # 30 daqiqa amal qiladi
        return JsonResponse({'success': True, 'redirect_url': '/billing/admin/'})

    return JsonResponse({'success': False, 'error': "Login yoki parol noto'g'ri"}, status=400)


def _require_admin_session(request):
    return request.session.get(ADMIN_SESSION_KEY, False)


# ---------------------------------------------------------------------
# 3) SUPERADMIN TAHRIRLASH PANELI
# ---------------------------------------------------------------------
def admin_panel(request):
    if not _require_admin_session(request):
        return redirect('billing:status')

    subscription = Subscription.get_solo()

    if request.method == 'POST':
        form = SubscriptionEditForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('billing:admin-panel')
    else:
        form = SubscriptionEditForm(instance=subscription)

    pending_receipts = PaymentReceipt.objects.filter(status=PaymentReceipt.STATUS_PENDING)
    history_receipts = PaymentReceipt.objects.exclude(status=PaymentReceipt.STATUS_PENDING)[:20]

    context = {
        'subscription': subscription,
        'student_count': subscription.get_student_count(),
        'total_amount': subscription.get_total_amount(),
        'form': form,
        'pending_receipts': pending_receipts,
        'history_receipts': history_receipts,
    }
    return render(request, 'billing/admin_panel.html', context)


@require_POST
def admin_approve_receipt(request, receipt_id):
    if not _require_admin_session(request):
        return redirect('billing:status')

    receipt = get_object_or_404(PaymentReceipt, pk=receipt_id)
    receipt.status = PaymentReceipt.STATUS_APPROVED
    receipt.reviewed_by = request.user if request.user.is_authenticated else None
    from django.utils import timezone
    receipt.reviewed_at = timezone.now()
    receipt.save()

    subscription = Subscription.get_solo()
    subscription.mark_paid()

    return redirect('billing:admin-panel')


@require_POST
def admin_reject_receipt(request, receipt_id):
    if not _require_admin_session(request):
        return redirect('billing:status')

    receipt = get_object_or_404(PaymentReceipt, pk=receipt_id)
    receipt.status = PaymentReceipt.STATUS_REJECTED
    receipt.reviewed_by = request.user if request.user.is_authenticated else None
    from django.utils import timezone
    receipt.reviewed_at = timezone.now()
    receipt.save()

    return redirect('billing:admin-panel')