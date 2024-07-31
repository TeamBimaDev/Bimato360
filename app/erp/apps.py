<<<<<<< HEAD
from django.apps import AppConfig


class ErpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'erp'

    def ready(self):
        from .sale_document import signals
        from .purchase_document import signals
        from .partner import signals
=======
from django.apps import AppConfig


class ErpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'erp'

    def ready(self):
        from .sale_document import signals
        from .purchase_document import signals
        from .partner import signals
>>>>>>> origin/ma-branch
