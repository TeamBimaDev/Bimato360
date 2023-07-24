from enum import Enum
from django.utils.translation import gettext_lazy as _


class CompanyType(Enum):
    SOLE_PROPRIETORSHIP = _('Sole proprietorship')
    GENERAL_PARTNERSHIP = _('General partnership')
    LIMITED_PARTNERSHIP = _('Limited partnership')
    PUBLIC_LIMITED_COMPANY_PLC = _('Public limited company(PLC)')
    LIMITED_LIABILITY_COMPANY_LLC = _('Limited liability company(LLC)')
    SIMPLIFIED_JOINT_STOCK = _('Simplified joint - stock')
    COMPANY_PARTNERSHIP_LIMITED_BY_SHARES = _('company Partnership limited by shares')
    COOPERATIVE_SOCIETY = _('Cooperative society')
    UNINCORPORATED_JOINT_VENTURE = _('Unincorporated joint venture')
    JOINT_STOCK_COMPANY = _('Joint - stock company')


def get_company_type_choices():
    return [(cp.name, cp.value) for cp in CompanyType]
