from common.enums.company_type import get_company_type_choices
from common.enums.entity_status import get_entity_status_choices
from common.enums.gender import get_gender_choices
from common.enums.partner_type import PartnerType
from common.enums.partner_type import get_partner_type_choices
from common.enums.transaction_enum import TransactionDirection
from core.abstract.models import AbstractModel
from core.address.models import return_parent_has_at_least_one_address
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class BimaErpPartner(AbstractModel):
    is_supplier = models.BooleanField(
        blank=True, null=True, verbose_name=_("Is Supplier")
    )
    is_customer = models.BooleanField(
        blank=True, null=True, verbose_name=_("Is Customer")
    )
    partner_type = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        choices=get_partner_type_choices(),
        verbose_name=_("Partner Type"),
    )
    company_type = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        choices=get_company_type_choices(),
        verbose_name=_("Company Type"),
    )
    first_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_("Last Name")
    )
    gender = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        choices=get_gender_choices(),
        verbose_name=_("Gender"),
    )
    social_security_number = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("Social Security Number")
    )
    id_number = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("ID Number")
    )
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(blank=True, null=True, verbose_name=_("Phone"))
    fax = models.CharField(blank=True, null=True, verbose_name=_("Fax"))
    company_name = models.CharField(
        blank=True, null=True, verbose_name=_("Company Name")
    )
    company_activity = models.CharField(
        blank=True, null=True, verbose_name=_("Company Activity")
    )
    vat_id_number = models.CharField(
        blank=True, null=True, verbose_name=_("VAT ID Number")
    )
    status = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        choices=get_entity_status_choices(),
        verbose_name=_("Status"),
    )
    note = models.CharField(blank=True, null=True, verbose_name=_("Note"))
    company_date_creation = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Company Date Creation")
    )
    company_siren = models.CharField(
        blank=True, null=True, verbose_name=_("Company Siren")
    )
    company_siret = models.CharField(
        blank=True, null=True, verbose_name=_("Company Siret")
    )
    company_date_registration = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Company Date Registration")
    )
    rcs_number = models.CharField(blank=True, null=True, verbose_name=_("RCS Number"))
    company_date_struck_off = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Company Date Struck Off")
    )
    company_ape_text = models.CharField(
        blank=True, null=True, verbose_name=_("Company APE Text")
    )
    company_ape_code = models.CharField(
        blank=True, null=True, verbose_name=_("Company APE Code")
    )
    company_capital = models.CharField(
        blank=True, null=True, verbose_name=_("Company Capital")
    )
    credit = models.DecimalField(
        max_digits=18, decimal_places=3, default=0, verbose_name=_("Credit")
    )
    balance = models.DecimalField(
        max_digits=18, decimal_places=3, default=0, verbose_name=_("Balance")
    )
    bank_accounts = GenericRelation("treasury.BimaTreasuryBankAccount")

    def update_balance(self):
        total_income = sum(
            transaction.amount
            for transaction in self.bimatreasurytransaction_set.filter(
                direction=TransactionDirection.INCOME.name
            )
        )
        total_expense = sum(
            transaction.amount
            for transaction in self.bimatreasurytransaction_set.filter(
                direction=TransactionDirection.OUTCOME.name
            )
        )
        self.balance = total_income - total_expense - self.credit
        self.save()

    def __str__(self):
        partner_full_name = f"{self.first_name} {self.last_name}" \
            if self.partner_type == PartnerType.INDIVIDUAL.name \
            else self.company_name
        return f"{self.public_id, self.partner_type, partner_full_name}"

    @property
    def partner_full_name(self):
        return (f"{self.first_name} {self.last_name}"
                if self.partner_type == PartnerType.INDIVIDUAL.name
                else self.company_name)

    @property
    def partner_has_at_least_one_address(self):
        return return_parent_has_at_least_one_address(self)

    class Meta:
        ordering = ["-created"]
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):
        self.validate_unique_data_if_company()
        self.validate_unique_data_if_individual()
        super().save(*args, **kwargs)

    def validate_unique_data_if_company(self):
        if self.partner_type != PartnerType.COMPANY.name:
            return True

        query = Q(company_siren=self.company_siren) | Q(
            company_siret=self.company_siret
        )

        if self.pk:
            query = query & ~Q(pk=self.pk)

        if BimaErpPartner.objects.filter(query).exists():
            raise ValidationError(_("N° siren & siret doit être unique"))

    def validate_unique_data_if_individual(self):
        if self.partner_type != PartnerType.INDIVIDUAL.name:
            return True

        query = Q(id_number=self.id_number) | Q(
            social_security_number=self.social_security_number
        )

        if self.pk:
            query = query & ~Q(pk=self.pk)

        if BimaErpPartner.objects.filter(query).exists():
            raise ValidationError(
                _("N° identité et N° sécurité sociale doit être unique")
            )

