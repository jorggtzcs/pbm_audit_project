from django.db import models


# Create your models here.
class Pharmacy(models.Model):
    npi_number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    state_license = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        verbose_name_plural = "Pharmacies"

    def __str__(self):
        return self.name


class Claim(models.Model):
    # this links the claim to a specific pharmacy
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    rx_number = models.CharField(max_length=50)
    drug_name = models.CharField(max_length=255)
    fill_date = models.DateField()
    billed_amount = models.DecimalField(max_digits=15, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2)

    # logic for the audit
    is_audited = models.BooleanField(default=False)

    is_flagged=models.BooleanField(default=False)
    audit_notes= models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Claim {self.rx_number} - {self.drug_name}"

    def check_for_audit(self):
        """
        Flag claim if the paid amount is significantly
        higher than the billed amount.
        """
        if self.paid_amount > self.billed_amount:
            return "Flagged: Overpayment"
        return "Clean"
