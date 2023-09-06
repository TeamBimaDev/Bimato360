import random

import faker
from common.enums.company_type import get_company_type_choices
from common.enums.entity_status import get_entity_status_choices
from common.enums.gender import get_gender_choices
from common.enums.partner_type import get_partner_type_choices
from common.enums.sale_document_enum import get_payment_status
from common.enums.sale_document_enum import get_sale_document_validity, get_sale_document_recurring_interval
from core.address.models import BimaCoreAddress
from core.country.models import BimaCoreCountry
from core.state.models import BimaCoreState
from django.contrib.contenttypes.models import ContentType
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from erp.sale_document.models import BimaErpSaleDocument, BimaErpSaleDocumentProduct

fake = faker.Faker()


def fake_bima_erp_sale_document(partner):
    payment_status = random.choice([x[0] for x in get_payment_status()])
    total_amount = 4500

    if payment_status == 'NOT_PAID':
        amount_paid = 0
    elif payment_status == 'PARTIAL_PAID':
        amount_paid = fake.random_int(min=1, max=(total_amount - 1))
    else:
        amount_paid = total_amount

    sale_document = BimaErpSaleDocument(
        id=fake.random_int(min=1, max=10),
        number=fake.random_number(digits=6, fix_len=True),
        date=fake.date_this_year(),
        status='CONFIRMED',
        type='INVOICE',
        partner=partner,
        vat_label="Euro",
        vat_amount=fake.random_int(min=1, max=40),
        note=fake.text(),
        private_note=fake.text(),
        validity=random.choice([x[0] for x in get_sale_document_validity()]),
        delivery_terms=fake.text(),
        total_amount_without_vat=fake.random_int(min=1, max=10),
        total_after_discount=fake.random_int(min=1, max=20),
        total_vat=fake.random_int(min=1, max=30),
        total_amount=total_amount,
        total_discount=fake.random_int(min=1, max=50),
        is_recurring=fake.boolean(),
        recurring_interval=random.choice([x[0] for x in get_sale_document_recurring_interval()]),
        payment_status=payment_status,
        amount_paid=amount_paid

    )
    return sale_document


def fake_bima_erp_sale_document_product(sale_document):
    product = BimaErpSaleDocumentProduct(
        id=fake.random_int(min=1, max=10000),
        sale_document=sale_document,
        product=BimaErpProduct.objects.order_by("?").first(),
        sale_document_public_id=fake.uuid4(),
        name=fake.name(),
        reference=fake.word(),
        quantity=fake.random_int(min=1, max=10),
        unit_of_measure='default',
        unit_price=fake.random_int(min=1, max=20),
        vat=fake.random_int(min=1, max=30),
        vat_amount=fake.random_int(min=1, max=40),
        discount=fake.random_int(min=1, max=50),
        discount_amount=fake.random_int(min=1, max=60),
        total_without_vat=fake.random_int(min=1, max=70),
        total_after_discount=fake.random_int(min=1, max=80),
        total_price=fake.random_int(min=1, max=90),
    )
    return product


def fake_bima_erp_partner():
    partner = BimaErpPartner(
        id=fake.random_int(min=1, max=10),
        is_supplier=fake.boolean(),
        is_customer=fake.boolean(),
        partner_type=random.choice([x[0] for x in get_partner_type_choices()]),
        company_type=random.choice([x[0] for x in get_company_type_choices()]),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        gender=random.choice([x[0] for x in get_gender_choices()]),
        social_security_number=fake.ssn(),
        id_number=fake.random_number(digits=8),
        email=fake.email(),
        phone=fake.phone_number(),
        fax=fake.phone_number(),
        company_name=fake.company(),
        company_activity=fake.job(),
        vat_id_number=fake.random_number(digits=8),
        status=random.choice([x[0] for x in get_entity_status_choices()]),
        note=fake.text(),
        company_date_creation=fake.date_this_year(),
        company_siren=fake.random_number(digits=8),
        company_siret=fake.random_number(digits=14),
        company_date_registration=fake.date_this_year(),
        rcs_number=fake.random_number(digits=8),
        company_date_struck_off=fake.date_this_year(),
        company_ape_text=fake.text(),
        company_ape_code=fake.random_number(digits=5),
        company_capital=fake.random_number(digits=5),
        credit=fake.pydecimal(right_digits=3, positive=True),
        balance=fake.pydecimal(right_digits=3, positive=True),
    )
    return partner


def fake_bima_core_address():
    content_type = ContentType.objects.get_for_model(BimaErpPartner)
    parent_id = BimaErpPartner.objects.order_by("?").first().id
    address = BimaCoreAddress(
        id=fake.random_int(min=1, max=10),
        number=fake.building_number(),
        street=fake.street_name(),
        street2=fake.secondary_address(),
        zip=fake.zipcode(),
        city=fake.city(),
        contact_name=fake.name(),
        contact_phone=fake.phone_number(),
        contact_email=fake.email(),
        can_send_bill=fake.boolean(),
        can_deliver=fake.boolean(),
        latitude=fake.latitude(),
        longitude=fake.longitude(),
        note=fake.text(),
        state=BimaCoreState.objects.order_by("?").first(),
        country=BimaCoreCountry.objects.order_by("?").first(),
        parent_type=content_type,
        parent_id=parent_id,
    )
    return address


def generate_fake_data():
    fake_partner = fake_bima_erp_partner()
    fake_address = fake_bima_core_address()
    fake_sale_document = fake_bima_erp_sale_document(fake_partner)
    fake_products = [fake_bima_erp_sale_document_product(fake_sale_document) for _ in range(4)]

    return {
        'sale_document': fake_sale_document,
        'partner': fake_partner,
        'address': fake_address,
        'products': fake_products
    }
