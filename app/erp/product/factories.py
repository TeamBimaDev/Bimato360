<<<<<<< HEAD
import factory
from common.enums.product_enum import get_product_types, \
    get_product_price_calculation_method, \
    get_product_status
from erp.category.factories import BimaErpCategoryFactory
from erp.unit_of_measure.factories import BimaErpUnitOfMeasureFactory
from erp.vat.factories import BimaErpVatFactory

from .models import BimaErpProduct


class BimaErpProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpProduct

    name = factory.Faker('name')
    reference = factory.Sequence(lambda n: f"REF_{n}")
    description = factory.Faker('text')
    ean13 = factory.Faker('ean13')
    type = factory.Faker('random_element', elements=get_product_types())
    purchase_price = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    sell_price = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    price_calculation_method = factory.Faker('random_element', elements=get_product_price_calculation_method())
    sell_percentage = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, max_value=100)
    category = factory.SubFactory(BimaErpCategoryFactory)
    vat = factory.SubFactory(BimaErpVatFactory)
    unit_of_measure = factory.SubFactory(BimaErpUnitOfMeasureFactory)
    status = factory.Faker('random_element', elements=get_product_status())
    minimum_stock_level = factory.Faker('pyint', min_value=0, max_value=100)
    maximum_stock_level = factory.Faker('pyint', min_value=100, max_value=200)
    dimension = factory.Faker('word')
    weight = factory.Faker('word')
    reorder_point = factory.Faker('pyint', min_value=0, max_value=100)
    lead_time = factory.Faker('pyint', min_value=1, max_value=30)
    serial_number = factory.Faker('word')
    quantity = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    virtual_quantity = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
=======
import factory
from common.enums.product_enum import get_product_types, \
    get_product_price_calculation_method, \
    get_product_status
from erp.category.factories import BimaErpCategoryFactory
from erp.unit_of_measure.factories import BimaErpUnitOfMeasureFactory
from erp.vat.factories import BimaErpVatFactory

from .models import BimaErpProduct


class BimaErpProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaErpProduct

    name = factory.Faker('name')
    reference = factory.Sequence(lambda n: f"REF_{n}")
    description = factory.Faker('text')
    ean13 = factory.Faker('ean13')
    type = factory.Faker('random_element', elements=get_product_types())
    purchase_price = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    sell_price = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    price_calculation_method = factory.Faker('random_element', elements=get_product_price_calculation_method())
    sell_percentage = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True, max_value=100)
    category = factory.SubFactory(BimaErpCategoryFactory)
    vat = factory.SubFactory(BimaErpVatFactory)
    unit_of_measure = factory.SubFactory(BimaErpUnitOfMeasureFactory)
    status = factory.Faker('random_element', elements=get_product_status())
    minimum_stock_level = factory.Faker('pyint', min_value=0, max_value=100)
    maximum_stock_level = factory.Faker('pyint', min_value=100, max_value=200)
    dimension = factory.Faker('word')
    weight = factory.Faker('word')
    reorder_point = factory.Faker('pyint', min_value=0, max_value=100)
    lead_time = factory.Faker('pyint', min_value=1, max_value=30)
    serial_number = factory.Faker('word')
    quantity = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    virtual_quantity = factory.Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
>>>>>>> origin/ma-branch
