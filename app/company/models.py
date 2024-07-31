<<<<<<< HEAD
import pytz
from common.enums.font_family import get_font_family_list
from common.enums.language import LanguageEnum
from core.abstract.models import AbstractModel
from core.currency.models import BimaCoreCurrency
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaCompany(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    mobile = models.CharField(max_length=32, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=2, choices=LanguageEnum.choices, default=LanguageEnum.ENGLISH)
    currency = models.ForeignKey(BimaCoreCurrency, on_delete=models.PROTECT)
    timezone = models.CharField(max_length=32, choices=[(tz, tz) for tz in pytz.all_timezones], default='UTC')
    header_note = models.TextField(blank=True, null=True)
    footer_note = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Company Date Creation'))
    siren = models.CharField(blank=True, null=True, verbose_name=_('Company Siren'))
    siret = models.CharField(blank=True, null=True, verbose_name=_('Company Siret'))
    date_registration = models.DateTimeField(blank=True, null=True, verbose_name=_('Company Date Registration'))
    rcs_number = models.CharField(blank=True, null=True, verbose_name=_('RCS Number'))
    date_struck_off = models.DateTimeField(blank=True, null=True, verbose_name=_('Company Date Struck Off'))
    ape_text = models.CharField(blank=True, null=True, verbose_name=_('Company APE Text'))
    ape_code = models.CharField(blank=True, null=True, verbose_name=_('Company APE Code'))
    capital = models.CharField(blank=True, null=True, verbose_name=_('Company Capital'))
    default_pdf_invoice_format = models.CharField(blank=True, null=True, default='sale_document_elegant.html',
                                                  verbose_name=_('Default Invoice format'))
    default_font_family = models.CharField(blank=True, null=True, default='Arial',
                                           verbose_name=_('Police par défaut'),
                                           choices=get_font_family_list())
    show_template_header = models.BooleanField(default=True, blank=True, null=True, verbose_name=_("Afficher l'entête"))
    show_template_footer = models.BooleanField(default=True, null=True, blank=True,
                                               verbose_name=_("Afficher le pieds de page"))
    show_template_logo = models.BooleanField(default=True, null=True, blank=True, verbose_name=_("Afficher le logo"))
    default_color = models.CharField(blank=True, null=True, default='#000000',
                                     verbose_name=_('Couleur par défaut'))
    bank_accounts = GenericRelation('treasury.BimaTreasuryBankAccount')

    vacation_coefficient = models.FloatField(default=1.82)
    start_working_day = models.PositiveSmallIntegerField(
        choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
                 (6, 'Sunday')], default=0)
    end_working_day = models.PositiveSmallIntegerField(
        choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
                 (6, 'Sunday')], default=4)

    def __str__(self):
        return f"{self.name, self.public_id}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
=======
import pytz
from common.enums.font_family import get_font_family_list
from common.enums.language import LanguageEnum
from core.abstract.models import AbstractModel
from core.currency.models import BimaCoreCurrency
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaCompany(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    mobile = models.CharField(max_length=32, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=2, choices=LanguageEnum.choices, default=LanguageEnum.ENGLISH)
    currency = models.ForeignKey(BimaCoreCurrency, on_delete=models.PROTECT)
    timezone = models.CharField(max_length=32, choices=[(tz, tz) for tz in pytz.all_timezones], default='UTC')
    header_note = models.TextField(blank=True, null=True)
    footer_note = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Company Date Creation'))
    siren = models.CharField(blank=True, null=True, verbose_name=_('Company Siren'))
    siret = models.CharField(blank=True, null=True, verbose_name=_('Company Siret'))
    date_registration = models.DateTimeField(blank=True, null=True, verbose_name=_('Company Date Registration'))
    rcs_number = models.CharField(blank=True, null=True, verbose_name=_('RCS Number'))
    date_struck_off = models.DateTimeField(blank=True, null=True, verbose_name=_('Company Date Struck Off'))
    ape_text = models.CharField(blank=True, null=True, verbose_name=_('Company APE Text'))
    ape_code = models.CharField(blank=True, null=True, verbose_name=_('Company APE Code'))
    capital = models.CharField(blank=True, null=True, verbose_name=_('Company Capital'))
    default_pdf_invoice_format = models.CharField(blank=True, null=True, default='sale_document_elegant.html',
                                                  verbose_name=_('Default Invoice format'))
    default_font_family = models.CharField(blank=True, null=True, default='Arial',
                                           verbose_name=_('Police par défaut'),
                                           choices=get_font_family_list())
    show_template_header = models.BooleanField(default=True, blank=True, null=True, verbose_name=_("Afficher l'entête"))
    show_template_footer = models.BooleanField(default=True, null=True, blank=True,
                                               verbose_name=_("Afficher le pieds de page"))
    show_template_logo = models.BooleanField(default=True, null=True, blank=True, verbose_name=_("Afficher le logo"))
    default_color = models.CharField(blank=True, null=True, default='#000000',
                                     verbose_name=_('Couleur par défaut'))
    bank_accounts = GenericRelation('treasury.BimaTreasuryBankAccount')

    vacation_coefficient = models.FloatField(default=1.82)
    start_working_day = models.PositiveSmallIntegerField(
        choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
                 (6, 'Sunday')], default=0)
    end_working_day = models.PositiveSmallIntegerField(
        choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
                 (6, 'Sunday')], default=4)

    def __str__(self):
        return f"{self.name, self.public_id}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
>>>>>>> origin/ma-branch
