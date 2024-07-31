<<<<<<< HEAD
from decimal import Decimal


class Bima360Helper:
    @staticmethod
    def truncate(number, decimal_places=2):
        factor = Decimal(10) ** decimal_places
        return (Decimal(number) * factor).to_integral_value() / factor
=======
from decimal import Decimal


class Bima360Helper:
    @staticmethod
    def truncate(number, decimal_places=2):
        factor = Decimal(10) ** decimal_places
        return (Decimal(number) * factor).to_integral_value() / factor
>>>>>>> origin/ma-branch
