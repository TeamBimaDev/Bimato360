class PermissionsList:
    CORE_BANK_CREATE = ('core.bank.can_create', 'Can create bank')
    CORE_BANK_UPDATE = ('core.bank.can_update', 'Can update bank')
    CORE_BANK_DELETE = ('core.bank.can_delete', 'Can delete bank')
    CORE_BANK_READ = ('core.bank.can_read', 'Can read bank')

    CORE_CONTACT_CREATE = ('core.contact.can_create', 'Can create contact')
    CORE_CONTACT_UPDATE = ('core.contact.can_update', 'Can update contact')
    CORE_CONTACT_DELETE = ('core.contact.can_delete', 'Can delete contact')
    CORE_CONTACT_READ = ('core.contact.can_read', 'Can read contact')

    CORE_COUNTRY_CREATE = ('core.country.can_create', 'Can create country')
    CORE_COUNTRY_UPDATE = ('core.country.can_update', 'Can update country')
    CORE_COUNTRY_DELETE = ('core.country.can_delete', 'Can delete country')
    CORE_COUNTRY_READ = ('core.country.can_read', 'Can read country')

    CORE_CURRENCY_CREATE = ('core.currency.can_create', 'Can create currency')
    CORE_CURRENCY_UPDATE = ('core.currency.can_update', 'Can update currency')
    CORE_CURRENCY_DELETE = ('core.currency.can_delete', 'Can delete currency')
    CORE_CURRENCY_READ = ('core.currency.can_read', 'Can read currency')

    CORE_DEPARTMENT_CREATE = ('core.department.can_create', 'Can create department')
    CORE_DEPARTMENT_UPDATE = ('core.department.can_update', 'Can update department')
    CORE_DEPARTMENT_DELETE = ('core.department.can_delete', 'Can delete department')
    CORE_DEPARTMENT_READ = ('core.department.can_read', 'Can read department')

    CORE_DOCUMENT_CREATE = ('core.document.can_create', 'Can create document')
    CORE_DOCUMENT_UPDATE = ('core.document.can_update', 'Can update document')
    CORE_DOCUMENT_DELETE = ('core.document.can_delete', 'Can delete document')
    CORE_DOCUMENT_READ = ('core.document.can_read', 'Can read document')

    CORE_ENTITY_TAG_CREATE = ('core.entity_tag.can_create', 'Can create entity tag')
    CORE_ENTITY_TAG_UPDATE = ('core.entity_tag.can_update', 'Can update entity tag')
    CORE_ENTITY_TAG_DELETE = ('core.entity_tag.can_delete', 'Can delete entity tag')
    CORE_ENTITY_TAG_READ = ('core.entity_tag.can_read', 'Can read entity tag')

    CORE_POST_CREATE = ('core.post.can_create', 'Can create post')
    CORE_POST_UPDATE = ('core.post.can_update', 'Can update post')
    CORE_POST_DELETE = ('core.post.can_delete', 'Can delete post')
    CORE_POST_READ = ('core.post.can_read', 'Can read post')

    CORE_SOURCE_CREATE = ('core.source.can_create', 'Can create source')
    CORE_SOURCE_UPDATE = ('core.source.can_update', 'Can update source')
    CORE_SOURCE_DELETE = ('core.source.can_delete', 'Can delete source')
    CORE_SOURCE_READ = ('core.source.can_read', 'Can read source')

    CORE_STATE_CREATE = ('core.state.can_create', 'Can create state')
    CORE_STATE_UPDATE = ('core.state.can_update', 'Can update state')
    CORE_STATE_DELETE = ('core.state.can_delete', 'Can delete state')
    CORE_STATE_READ = ('core.state.can_read', 'Can read state')

    CORE_TAG_CREATE = ('core.tag.can_create', 'Can create tag')
    CORE_TAG_UPDATE = ('core.tag.can_update', 'Can update tag')
    CORE_TAG_DELETE = ('core.tag.can_delete', 'Can delete tag')
    CORE_TAG_READ = ('core.tag.can_read', 'Can read tag')

    CORE_CASH_CREATE = ('core.cash.can_create', 'Can create cash')
    CORE_CASH_UPDATE = ('core.cash.can_update', 'Can update cash')
    CORE_CASH_DELETE = ('core.cash.can_delete', 'Can delete cash')
    CORE_CASH_READ = ('core.cash.can_read', 'Can read cash')

    ERP_CATEGORY_CREATE = ('erp.category.can_create', 'Can create category')
    ERP_CATEGORY_UPDATE = ('erp.category.can_update', 'Can update category')
    ERP_CATEGORY_DELETE = ('erp.category.can_delete', 'Can delete category')
    ERP_CATEGORY_READ = ('erp.category.can_read', 'Can read category')

    ERP_PARTNER_CREATE = ('erp.partner.can_create', 'Can create partner')
    ERP_PARTNER_UPDATE = ('erp.partner.can_update', 'Can update partner')
    ERP_PARTNER_DELETE = ('erp.partner.can_delete', 'Can delete partner')
    ERP_PARTNER_READ = ('erp.partner.can_read', 'Can read partner')

    ERP_PAYMENT_TERMS_CREATE = ('erp.payment_terms.can_create', 'Can create payment terms')
    ERP_PAYMENT_TERMS_UPDATE = ('erp.payment_terms.can_update', 'Can update payment terms')
    ERP_PAYMENT_TERMS_DELETE = ('erp.payment_terms.can_delete', 'Can delete payment terms')
    ERP_PAYMENT_TERMS_READ = ('erp.payment_terms.can_read', 'Can read payment terms')

    ERP_PRODUCT_CREATE = ('erp.product.can_create', 'Can create product')
    ERP_PRODUCT_UPDATE = ('erp.product.can_update', 'Can update product')
    ERP_PRODUCT_DELETE = ('erp.product.can_delete', 'Can delete product')
    ERP_PRODUCT_READ = ('erp.product.can_read', 'Can read product')

    ERP_SALE_DOCUMENT_CREATE = ('erp.sale_document.can_create', 'Can create sale document')
    ERP_SALE_DOCUMENT_UPDATE = ('erp.sale_document.can_update', 'Can update sale document')
    ERP_SALE_DOCUMENT_DELETE = ('erp.sale_document.can_delete', 'Can delete sale document')
    ERP_SALE_DOCUMENT_READ = ('erp.sale_document.can_read', 'Can read sale document')

    ERP_SALE_DOCUMENT_ADD_PRODUCT = ('erp.sale_document.can_add_product',
                                     'Can add product to sale document')
    ERP_SALE_DOCUMENT_DELETE_PRODUCT = ('erp.sale_document.can_delete_product',
                                        'Can delete product from sale document')
    ERP_SALE_DOCUMENT_CHANGE_STATUS = ('erp.sale_document.can_change_status',
                                       'Can change status of sale document')
    ERP_SALE_DOCUMENT_ROLLBACK_STATUS = ('erp.sale_document.can_rollback_status',
                                         'Can rollback status of sale document')
    ERP_SALE_DOCUMENT_GENERATE_DOCUMENT = ('erp.sale_document.can_generate_document',
                                           'Can generate document from sale document')
    ERP_SALE_DOCUMENT_VIEW_HISTORY = ('erp.sale_document.can_view_history',
                                      'Can view history of sale document')

    ERP_PURCHASE_DOCUMENT_CREATE = ('erp.purchase_document.can_create', 'Can create purchase document')
    ERP_PURCHASE_DOCUMENT_UPDATE = ('erp.purchase_document.can_update', 'Can update purchase document')
    ERP_PURCHASE_DOCUMENT_DELETE = ('erp.purchase_document.can_delete', 'Can delete purchase document')
    ERP_PURCHASE_DOCUMENT_READ = ('erp.purchase_document.can_read', 'Can read purchase document')

    ERP_PURCHASE_DOCUMENT_ADD_PRODUCT = ('erp.purchase_document.can_add_product',
                                         'Can add product to purchase document')
    ERP_PURCHASE_DOCUMENT_DELETE_PRODUCT = ('erp.purchase_document.can_delete_product',
                                            'Can delete product from purchase document')
    ERP_PURCHASE_DOCUMENT_CHANGE_STATUS = ('erp.purchase_document.can_change_status',
                                           'Can change status of purchase document')
    ERP_PURCHASE_DOCUMENT_ROLLBACK_STATUS = ('erp.purchase_document.can_rollback_status',
                                             'Can rollback status of purchase document')
    ERP_PURCHASE_DOCUMENT_GENERATE_DOCUMENT = ('erp.purchase_document.can_generate_document',
                                               'Can generate document from purchase document')
    ERP_PURCHASE_DOCUMENT_VIEW_HISTORY = ('erp.purchase_document.can_view_history',
                                          'Can view history of purchase document')

    ERP_UNIT_OF_MEASURE_CREATE = ('erp.unit_of_measure.can_create', 'Can create unit of measure')
    ERP_UNIT_OF_MEASURE_UPDATE = ('erp.unit_of_measure.can_update', 'Can update unit of measure')
    ERP_UNIT_OF_MEASURE_DELETE = ('erp.unit_of_measure.can_delete', 'Can delete unit of measure')
    ERP_UNIT_OF_MEASURE_READ = ('erp.unit_of_measure.can_read', 'Can read unit of measure')

    ERP_VAT_CREATE = ('erp.vat.can_create', 'Can create vat')
    ERP_VAT_UPDATE = ('erp.vat.can_update', 'Can update vat')
    ERP_VAT_DELETE = ('erp.vat.can_delete', 'Can delete vat')
    ERP_VAT_READ = ('erp.vat.can_read', 'Can read vat')

    USER_USER_CREATE = ('user.user.can_create', 'Can create user')
    USER_USER_UPDATE = ('user.user.can_update', 'Can update user')
    USER_USER_DELETE = ('user.user.can_delete', 'Can delete user')
    USER_USER_READ = ('user.user.can_read', 'Can read user')
    USER_USER_ADD_PERMISSION = ('user.user.can_add_permission', 'Can add permission to user')
    USER_USER_UPDATE_OTHER_PASSWORD = ('user.user.can_edit_other_password', 'Can update other password')
    USER_USER_ACTIVATE_ACCOUNT = ('user.user.can_activate_account', 'Can activate new created user account')

