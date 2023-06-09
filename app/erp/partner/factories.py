import factory
from .models import BimaErpPartner
from common.enums.partner_type import get_partner_type_choices
from common.enums.company_type import get_company_type_choices
from common.enums.gender import get_gender_choices
from common.enums.entity_status import get_entity_status_choices


class BimaErpPartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpPartner

    is_supplier = factory.Faker('boolean')
    is_customer = factory.Faker('boolean')
    partner_type = factory.Faker('random_element', elements=[choice[0] for choice in get_partner_type_choices()])
    company_type = factory.Faker('random_element', elements=[choice[0] for choice in get_company_type_choices()])
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    gender = factory.Faker('random_element', elements=[choice[0] for choice in get_gender_choices()])
    social_security_number = factory.Faker('text')
    id_number = factory.Faker('text')
    email = factory.Faker('email')
    phone = factory.Faker('text')
    fax = factory.Faker('text')
    company_name = factory.Faker('text')
    company_activity = factory.Faker('text')
    vat_id_number = factory.Faker('text')
    status = factory.Faker('random_element', elements=[choice[0] for choice in get_entity_status_choices()])
    note = factory.Faker('text')
    company_date_creation = factory.Faker('date')
    company_siren = factory.Faker('text')
    company_siret = factory.Faker('text')
    company_date_registration = factory.Faker('date')
    rcs_number = factory.Faker('text')
    company_date_struck_off = factory.Faker('date')
    company_ape_text = factory.Faker('text')
    company_ape_code = factory.Faker('text')
    company_capital = factory.Faker('text')

