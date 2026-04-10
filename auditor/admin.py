from django.contrib import admin
from .models import Pharmacy, Claim


# Register your models here.
@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('npi_number', 'name', 'state_license')
    search_fields = ('name', 'npi_number')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('rx_number', 'pharmacy', 'drug_name', 'billed_amount', 'paid_amount', 'is_audited')
    list_filter = ('is_audited', 'fill_date')
    # This adds a search bar for the pharmacy name or drug name
    search_fields = ('drug_name', 'pharmacy__name')
