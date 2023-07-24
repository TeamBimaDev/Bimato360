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
    partner_type = factory.Faker('random_element', elements=get_partner_type_choices())
    company_type = factory.Faker('random_element', elements=get_company_type_choices())
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    gender = factory.Faker('random_element', elements=get_gender_choices())
    social_security_number = factory.Faker('ssn')
    id_number = factory.Faker('random_number', digits=8)
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    fax = factory.Faker('phone_number')
    company_name = factory.Faker('company')
    company_activity = factory.Faker('job')
    vat_id_number = factory.Faker('random_number', digits=10)
    status = factory.Faker('random_element', elements=get_entity_status_choices())
    note = factory.Faker('text')
    company_date_creation = factory.Faker('date_time')
    company_siren = factory.Faker('random_number', digits=9)
    company_siret = factory.Faker('random_number', digits=14)
    company_date_registration = factory.Faker('date_time')
    rcs_number = factory.Faker('random_number', digits=9)
    company_date_struck_off = factory.Faker('date_time')
    company_ape_text = factory.Faker('job')
    company_ape_code = factory.Faker('random_number', digits=4)
    company_capital = factory.Faker('random_number', digits=6)
    credit = factory.Faker('pydecimal', right_digits=3, positive=True, max_value=100000)
    balance = factory.Faker('pydecimal', right_digits=3, positive=True, max_value=100000)


