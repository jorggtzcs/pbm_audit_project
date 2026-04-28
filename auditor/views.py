from django.shortcuts import render
from django.core.management import call_command
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Claim


# Create your views here.
def audit_dashboard(request):
    # Run the audit logic
    all_claims = Claim.objects.all()
    for claim in all_claims:
        if claim.paid_amount > claim.billed_amount:
            claim.is_flagged = True
            claim.audit_notes = "Overpayment detected: Paid>Billed"
            claim.save()

    # Calculate Stats
    stats = {
        'total_claims': all_claims.count(),
        'flagged_count': Claim.objects.filter(is_flagged=True).count(),
        'total_billed': all_claims.aggregate(Sum('billed_amount'))['billed_amount__sum'],
        'potential_savings': Claim.objects.filter(is_flagged=True).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    }

    return render(request, 'auditor/dashboard.html', {'stats': stats})
