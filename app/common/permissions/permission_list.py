class PermissionsList:
    CORE_BANK_CREATE = ("core.bank.can_create", "Can create bank", "CORE_BANK")
    CORE_BANK_UPDATE = ("core.bank.can_update", "Can update bank", "CORE_BANK")
    CORE_BANK_DELETE = ("core.bank.can_delete", "Can delete bank", "CORE_BANK")
    CORE_BANK_READ = ("core.bank.can_read", "Can read bank", "CORE_BANK")

    CORE_ADDRESS_CREATE = (
        "core.address.can_create",
        "Can create address",
        "CORE_ADDRESS",
    )
    CORE_ADDRESS_UPDATE = (
        "core.address.can_update",
        "Can update address",
        "CORE_ADDRESS",
    )
    CORE_ADDRESS_DELETE = (
        "core.address.can_delete",
        "Can delete address",
        "CORE_ADDRESS",
    )
    CORE_ADDRESS_READ = ("core.address.can_read", "Can read address", "CORE_ADDRESS")

    CORE_CONTACT_CREATE = (
        "core.contact.can_create",
        "Can create contact",
        "CORE_CONTACT",
    )
    CORE_CONTACT_UPDATE = (
        "core.contact.can_update",
        "Can update contact",
        "CORE_CONTACT",
    )
    CORE_CONTACT_DELETE = (
        "core.contact.can_delete",
        "Can delete contact",
        "CORE_CONTACT",
    )
    CORE_CONTACT_READ = ("core.contact.can_read", "Can read contact", "CORE_CONTACT")

    CORE_COUNTRY_CREATE = (
        "core.country.can_create",
        "Can create country",
        "CORE_COUNTRY",
    )
    CORE_COUNTRY_UPDATE = (
        "core.country.can_update",
        "Can update country",
        "CORE_COUNTRY",
    )
    CORE_COUNTRY_DELETE = (
        "core.country.can_delete",
        "Can delete country",
        "CORE_COUNTRY",
    )
    CORE_COUNTRY_READ = ("core.country.can_read", "Can read country", "CORE_COUNTRY")

    CORE_CURRENCY_CREATE = (
        "core.currency.can_create",
        "Can create currency",
        "CORE_CURRENCY",
    )
    CORE_CURRENCY_UPDATE = (
        "core.currency.can_update",
        "Can update currency",
        "CORE_CURRENCY",
    )
    CORE_CURRENCY_DELETE = (
        "core.currency.can_delete",
        "Can delete currency",
        "CORE_CURRENCY",
    )
    CORE_CURRENCY_READ = (
        "core.currency.can_read",
        "Can read currency",
        "CORE_CURRENCY",
    )

    CORE_DEPARTMENT_CREATE = (
        "core.department.can_create",
        "Can create department",
        "CORE_DEPARTMENT",
    )
    CORE_DEPARTMENT_UPDATE = (
        "core.department.can_update",
        "Can update department",
        "CORE_DEPARTMENT",
    )
    CORE_DEPARTMENT_DELETE = (
        "core.department.can_delete",
        "Can delete department",
        "CORE_DEPARTMENT",
    )
    CORE_DEPARTMENT_READ = (
        "core.department.can_read",
        "Can read department",
        "CORE_DEPARTMENT",
    )

    CORE_DOCUMENT_CREATE = (
        "core.document.can_create",
        "Can create document",
        "CORE_DOCUMENT",
    )
    CORE_DOCUMENT_UPDATE = (
        "core.document.can_update",
        "Can update document",
        "CORE_DOCUMENT",
    )
    CORE_DOCUMENT_DELETE = (
        "core.document.can_delete",
        "Can delete document",
        "CORE_DOCUMENT",
    )
    CORE_DOCUMENT_READ = (
        "core.document.can_read",
        "Can read document",
        "CORE_DOCUMENT",
    )

    CORE_ENTITY_TAG_CREATE = (
        "core.entity_tag.can_create",
        "Can create entity tag",
        "CORE_ENTITY_TAG",
    )
    CORE_ENTITY_TAG_UPDATE = (
        "core.entity_tag.can_update",
        "Can update entity tag",
        "CORE_ENTITY_TAG",
    )
    CORE_ENTITY_TAG_DELETE = (
        "core.entity_tag.can_delete",
        "Can delete entity tag",
        "CORE_ENTITY_TAG",
    )
    CORE_ENTITY_TAG_READ = (
        "core.entity_tag.can_read",
        "Can read entity tag",
        "CORE_ENTITY_TAG",
    )

    CORE_SOURCE_CREATE = ("core.source.can_create", "Can create source", "CORE_SOURCE")
    CORE_SOURCE_UPDATE = ("core.source.can_update", "Can update source", "CORE_SOURCE")
    CORE_SOURCE_DELETE = ("core.source.can_delete", "Can delete source", "CORE_SOURCE")
    CORE_SOURCE_READ = ("core.source.can_read", "Can read source", "CORE_SOURCE")

    CORE_STATE_CREATE = ("core.state.can_create", "Can create state", "CORE_STATE")
    CORE_STATE_UPDATE = ("core.state.can_update", "Can update state", "CORE_STATE")
    CORE_STATE_DELETE = ("core.state.can_delete", "Can delete state", "CORE_STATE")
    CORE_STATE_READ = ("core.state.can_read", "Can read state", "CORE_STATE")

    CORE_TAG_CREATE = ("core.tag.can_create", "Can create tag", "CORE_TAG")
    CORE_TAG_UPDATE = ("core.tag.can_update", "Can update tag", "CORE_TAG")
    CORE_TAG_DELETE = ("core.tag.can_delete", "Can delete tag", "CORE_TAG")
    CORE_TAG_READ = ("core.tag.can_read", "Can read tag", "CORE_TAG")

    CORE_NOTIFICATION_CREATE = ("core.notification.can_create", "Can create notification", "CORE_NOTIFICATION")
    CORE_NOTIFICATION_READ = ("core.notification.can_read", "Can read notification", "CORE_NOTIFICATION")

    CORE_NOTIFICATION_TYPE_CREATE = (
        "core.notification_type.can_create", "Can create notification type", "CORE_NOTIFICATION_TYPE")
    CORE_NOTIFICATION_TYPE_UPDATE = (
        "core.notification_type.can_update", "Can update notification type", "CORE_NOTIFICATION_TYPE")
    CORE_NOTIFICATION_TYPE_DELETE = (
        "core.notification_type.can_delete", "Can delete notification type", "CORE_NOTIFICATION_TYPE")
    CORE_NOTIFICATION_TYPE_READ = (
        "core.notification_type.can_read", "Can read notification type", "CORE_NOTIFICATION_TYPE")

    CORE_NOTIFICATION_TEMPLATE_CREATE = (
        "core.notification_template.can_create", "Can create notification template", "CORE_NOTIFICATION_TEMPLATE")
    CORE_NOTIFICATION_TEMPLATE_UPDATE = (
        "core.notification_template.can_update", "Can update notification template", "CORE_NOTIFICATION_TEMPLATE")
    CORE_NOTIFICATION_TEMPLATE_DELETE = (
        "core.notification_template.can_delete", "Can delete notification template", "CORE_NOTIFICATION_TEMPLATE")
    CORE_NOTIFICATION_TEMPLATE_READ = (
        "core.notification_template.can_read", "Can read notification template", "CORE_NOTIFICATION_TEMPLATE")

    ERP_CATEGORY_CREATE = (
        "erp.category.can_create",
        "Can create category",
        "ERP_CATEGORY",
    )
    ERP_CATEGORY_UPDATE = (
        "erp.category.can_update",
        "Can update category",
        "ERP_CATEGORY",
    )
    ERP_CATEGORY_DELETE = (
        "erp.category.can_delete",
        "Can delete category",
        "ERP_CATEGORY",
    )
    ERP_CATEGORY_READ = ("erp.category.can_read", "Can read category", "ERP_CATEGORY")

    ERP_PARTNER_CREATE = ("erp.partner.can_create", "Can create partner", "ERP_PARTNER")
    ERP_PARTNER_UPDATE = ("erp.partner.can_update", "Can update partner", "ERP_PARTNER")
    ERP_PARTNER_DELETE = ("erp.partner.can_delete", "Can delete partner", "ERP_PARTNER")
    ERP_PARTNER_READ = ("erp.partner.can_read", "Can read partner", "ERP_PARTNER")

    ERP_PRODUCT_CREATE = ("erp.product.can_create", "Can create product", "ERP_PRODUCT")
    ERP_PRODUCT_UPDATE = ("erp.product.can_update", "Can update product", "ERP_PRODUCT")
    ERP_PRODUCT_DELETE = ("erp.product.can_delete", "Can delete product", "ERP_PRODUCT")
    ERP_PRODUCT_READ = ("erp.product.can_read", "Can read product", "ERP_PRODUCT")

    ERP_SALE_DOCUMENT_CREATE = (
        "erp.sale_document.can_create",
        "Can create sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_UPDATE = (
        "erp.sale_document.can_update",
        "Can update sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_DELETE = (
        "erp.sale_document.can_delete",
        "Can delete sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_READ = (
        "erp.sale_document.can_read",
        "Can read sale document",
        "ERP_SALE_DOCUMENT",
    )

    ERP_SALE_DOCUMENT_ADD_PRODUCT = (
        "erp.sale_document.can_add_product",
        "Can add product to sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_UPDATE_PRODUCT = (
        "erp.sale_document.can_update_product",
        "Can update product in a sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_DELETE_PRODUCT = (
        "erp.sale_document.can_delete_product",
        "Can delete product from sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_CHANGE_STATUS = (
        "erp.sale_document.can_change_status",
        "Can change status of sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_ROLLBACK_STATUS = (
        "erp.sale_document.can_rollback_status",
        "Can rollback status of sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_GENERATE_DOCUMENT = (
        "erp.sale_document.can_generate_document",
        "Can generate document from sale document",
        "ERP_SALE_DOCUMENT",
    )
    ERP_SALE_DOCUMENT_VIEW_HISTORY = (
        "erp.sale_document.can_view_history",
        "Can view history of sale document",
        "ERP_SALE_DOCUMENT",
    )

    ERP_PURCHASE_DOCUMENT_CREATE = (
        "erp.purchase_document.can_create",
        "Can create purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_UPDATE = (
        "erp.purchase_document.can_update",
        "Can update purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_DELETE = (
        "erp.purchase_document.can_delete",
        "Can delete purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_READ = (
        "erp.purchase_document.can_read",
        "Can read purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )

    ERP_PURCHASE_DOCUMENT_ADD_PRODUCT = (
        "erp.purchase_document.can_add_product",
        "Can add product to purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_UPDATE_PRODUCT = (
        "erp.purchase_document.can_update_product",
        "Can update product in a purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_DELETE_PRODUCT = (
        "erp.purchase_document.can_delete_product",
        "Can delete product from purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_CHANGE_STATUS = (
        "erp.purchase_document.can_change_status",
        "Can change status of purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_ROLLBACK_STATUS = (
        "erp.purchase_document.can_rollback_status",
        "Can rollback status of purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_GENERATE_DOCUMENT = (
        "erp.purchase_document.can_generate_document",
        "Can generate document from purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )
    ERP_PURCHASE_DOCUMENT_VIEW_HISTORY = (
        "erp.purchase_document.can_view_history",
        "Can view history of purchase document",
        "ERP_PURCHASE_DOCUMENT",
    )

    ERP_UNIT_OF_MEASURE_CREATE = (
        "erp.unit_of_measure.can_create",
        "Can create unit of measure",
        "ERP_UNIT_OF_MEASURE",
    )
    ERP_UNIT_OF_MEASURE_UPDATE = (
        "erp.unit_of_measure.can_update",
        "Can update unit of measure",
        "ERP_UNIT_OF_MEASURE",
    )
    ERP_UNIT_OF_MEASURE_DELETE = (
        "erp.unit_of_measure.can_delete",
        "Can delete unit of measure",
        "ERP_UNIT_OF_MEASURE",
    )
    ERP_UNIT_OF_MEASURE_READ = (
        "erp.unit_of_measure.can_read",
        "Can read unit of measure",
        "ERP_UNIT_OF_MEASURE",
    )

    ERP_VAT_CREATE = ("erp.vat.can_create", "Can create vat", "ERP_VAT")
    ERP_VAT_UPDATE = ("erp.vat.can_update", "Can update vat", "ERP_VAT")
    ERP_VAT_DELETE = ("erp.vat.can_delete", "Can delete vat", "ERP_VAT")
    ERP_VAT_READ = ("erp.vat.can_read", "Can read vat", "ERP_VAT")

    USER_USER_CREATE = ("user.user.can_create", "Can create user", "USER_USER")
    USER_USER_UPDATE = ("user.user.can_update", "Can update user", "USER_USER")
    USER_USER_DELETE = ("user.user.can_delete", "Can delete user", "USER_USER")
    USER_USER_READ = ("user.user.can_read", "Can read user", "USER_USER")
    USER_USER_ADD_PERMISSION = (
        "user.user.can_add_permission",
        "Can add permission to user",
        "USER_USER",
    )
    USER_USER_UPDATE_OTHER_PASSWORD = (
        "user.user.can_edit_other_password",
        "Can update other password",
        "USER_USER",
    )
    USER_USER_ACTIVATE_ACCOUNT = (
        "user.user.can_activate_account",
        "Can activate new created user account",
        "USER_USER",
    )

    USER_ROLE_CREATE = ("user.role.can_create", "Can create role", "USER_ROLE")
    USER_ROLE_UPDATE = ("user.role.can_update", "Can update role", "USER_ROLE")
    USER_ROLE_DELETE = ("user.role.can_delete", "Can delete role", "USER_ROLE")
    USER_ROLE_READ = ("user.role.can_read", "Can read role", "USER_ROLE")

    COMPANY_COMPANY_CREATE = (
        "company.company.can_create",
        "Can create company",
        "COMPANY_COMPANY",
    )
    COMPANY_COMPANY_UPDATE = (
        "company.company.can_update",
        "Can update company",
        "COMPANY_COMPANY",
    )
    COMPANY_COMPANY_DELETE = (
        "company.company.can_delete",
        "Can delete company",
        "COMPANY_COMPANY",
    )
    COMPANY_COMPANY_READ = (
        "company.company.can_read",
        "Can read company",
        "COMPANY_COMPANY",
    )
    COMPANY_COMPANY_ADD_DOCUMENT = (
        "company.company.can_add_document",
        "Can add document",
        "COMPANY_COMPANY",
    )
    COMPANY_COMPANY_ADD_ADDRESS = (
        "company.company.can_add_address",
        "Can add address",
        "COMPANY_COMPANY",
    )

    COMPANY_COMPANY_ADD_BANK_ACCOUNT = (
        "company.company.can_add_bank_account",
        "Can add bank account",
        "COMPANY_COMPANY",
    )

    TREASURY_CASH_CREATE = (
        "treasury.cash.can_create",
        "Can create cash",
        "TREASURY_CASH",
    )
    TREASURY_CASH_UPDATE = (
        "treasury.cash.can_update",
        "Can update cash",
        "TREASURY_CASH",
    )
    TREASURY_CASH_DELETE = (
        "treasury.cash.can_delete",
        "Can delete cash",
        "TREASURY_CASH",
    )
    TREASURY_CASH_READ = ("treasury.cash.can_read", "Can read cash", "TREASURY_CASH")

    TREASURY_BANK_ACCOUNT_CREATE = (
        "treasury.bank_account.can_create",
        "Can create bank account",
        "TREASURY_BANK_ACCOUNT",
    )
    TREASURY_BANK_ACCOUNT_UPDATE = (
        "treasury.bank_account.can_update",
        "Can update bank account",
        "TREASURY_BANK_ACCOUNT",
    )
    TREASURY_BANK_ACCOUNT_DELETE = (
        "treasury.bank_account.can_delete",
        "Can delete bank account",
        "TREASURY_BANK_ACCOUNT",
    )
    TREASURY_BANK_ACCOUNT_READ = (
        "treasury.bank_account.can_read",
        "Can read bank account",
        "TREASURY_BANK_ACCOUNT",
    )

    TREASURY_PAYMENT_TERM_CREATE = (
        "treasury.payment_term.can_create",
        "Can create payment term",
        "TREASURY_PAYMENT_TERM",
    )
    TREASURY_PAYMENT_TERM_UPDATE = (
        "treasury.payment_term.can_update",
        "Can update payment term",
        "TREASURY_PAYMENT_TERM",
    )
    TREASURY_PAYMENT_TERM_DELETE = (
        "treasury.payment_term.can_delete",
        "Can delete payment term",
        "TREASURY_PAYMENT_TERM",
    )
    TREASURY_PAYMENT_TERM_READ = (
        "treasury.payment_term.can_read",
        "Can read payment term",
        "TREASURY_PAYMENT_TERM",
    )

    TREASURY_TRANSACTION_TYPE_CREATE = (
        "treasury.transaction_type.can_create",
        "Can create transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )
    TREASURY_TRANSACTION_TYPE_UPDATE = (
        "treasury.transaction_type.can_update",
        "Can update transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )
    TREASURY_TRANSACTION_TYPE_DELETE = (
        "treasury.transaction_type.can_delete",
        "Can delete transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )
    TREASURY_TRANSACTION_TYPE_READ = (
        "treasury.transaction_type.can_read",
        "Can read transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )

    TREASURY_TRANSACTION_CREATE = (
        "treasury.transaction.can_create",
        "Can create transaction",
        "TREASURY_TRANSACTION",
    )
    TREASURY_TRANSACTION_UPDATE = (
        "treasury.transaction.can_update",
        "Can update transaction",
        "TREASURY_TRANSACTION",
    )
    TREASURY_TRANSACTION_DELETE = (
        "treasury.transaction.can_delete",
        "Can delete transaction",
        "TREASURY_TRANSACTION",
    )
    TREASURY_TRANSACTION_READ = (
        "treasury.transaction.can_read",
        "Can read transaction",
        "TREASURY_TRANSACTION",
    )
    TREASURY_TRANSACTION_VIEW_HISTORY = (
        "treasury.transaction.can_view_history",
        "Can view history transaction",
        "TREASURY_TRANSACTION",
    )

    TREASURY_PAYMENT_METHOD_CREATE = (
        "treasury.payment_method.can_create",
        "Can create transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )
    TREASURY_PAYMENT_METHOD_UPDATE = (
        "treasury.payment_method.can_update",
        "Can update transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )
    TREASURY_PAYMENT_METHOD_DELETE = (
        "treasury.payment_method.can_delete",
        "Can delete transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )
    TREASURY_PAYMENT_METHOD_READ = (
        "treasury.payment_method.can_read",
        "Can read transaction type",
        "TREASURY_TRANSACTION_TYPE",
    )

    HR_EMPLOYEE_CREATE = ("hr.employee.can_create", "Can create employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_UPDATE = ("hr.employee.can_update", "Can update employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_DELETE = ("hr.employee.can_delete", "Can delete employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_READ = ("hr.employee.can_read", "Can read employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_ADD_DOCUMENT = ("hr.employee.can_add_document", "Can add document to employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_ADD_ADDRESS = ("hr.employee.can_add_address", "Can add address to employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_ADD_CONTACT = ("hr.employee.can_add_address", "Can add address to employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_ADD_BANK_ACCOUNT = (
        "hr.employee.can_add_bank_account", "Can add bank account to employee", "HR_EMPLOYEE",)
    HR_EMPLOYEE_MANAGE_SKILL = ("hr.employee.can_manage_skill", "Can manage employee skills", "HR_EMPLOYEE",)
    HR_EMPLOYEE_MANAGE_EXPERIENCE = (
        "hr.employee.can_manage_experience", "Can manage employee experience", "HR_EMPLOYEE",)

    HR_APPLICANT_CREATE = ("hr.applicant.can_create", "Can create applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_UPDATE = ("hr.applicant.can_update", "Can update applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_DELETE = ("hr.applicant.can_delete", "Can delete applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_READ = ("hr.applicant.can_read", "Can read applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_ADD_DOCUMENT = ("hr.applicant.can_add_document", "Can add document to applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_ADD_ADDRESS = ("hr.applicant.can_add_address", "Can add address to applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_ADD_CONTACT = ("hr.applicant.can_add_address", "Can add address to applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_ADD_BANK_ACCOUNT = (
        "hr.applicant.can_add_bank_account", "Can add bank account to applicant", "HR_EMPLOYEE",)
    HR_APPLICANT_MANAGE_SKILL = ("hr.applicant.can_manage_skill", "Can manage applicant skills", "HR_APPLICANT",)
    HR_APPLICANT_MANAGE_EXPERIENCE = (
        "hr.applicant.can_manage_experience", "Can manage applicant experience", "HR_APPLICANT",)

    HR_SKILL_CATEGORY_CREATE = ("hr.skill_category.can_create", "Can create skill category", "HR_SKILL_CATEGORY",)
    HR_SKILL_CATEGORY_UPDATE = ("hr.skill_category.can_update", "Can update skill category", "HR_SKILL_CATEGORY",)
    HR_SKILL_CATEGORY_DELETE = ("hr.skill_category.can_delete", "Can delete skill category", "HR_SKILL_CATEGORY",)
    HR_SKILL_CATEGORY_READ = ("hr.skill_category.can_read", "Can read skill category", "HR_SKILL_CATEGORY")

    HR_SKILL_CREATE = ("hr.skill.can_create", "Can create skill", "HR_SKILL",)
    HR_SKILL_UPDATE = ("hr.skill.can_update", "Can update skill", "HR_SKILL",)
    HR_SKILL_DELETE = ("hr.skill.can_delete", "Can delete skill", "HR_SKILL",)
    HR_SKILL_READ = ("hr.skill.can_read", "Can read skill", "HR_SKILL")

    HR_JOB_CATEGORY_CREATE = ("hr.job_category.can_create", "Can create job category", "HR_JOB_CATEGORY",)
    HR_JOB_CATEGORY_UPDATE = ("hr.job_category.can_update", "Can update job category", "HR_JOB_CATEGORY",)
    HR_JOB_CATEGORY_DELETE = ("hr.job_category.can_delete", "Can delete job category", "HR_JOB_CATEGORY",)
    HR_JOB_CATEGORY_READ = ("hr.job_category.can_read", "Can read job category", "HR_JOB_CATEGORY")

    HR_POSITION_CREATE = ("hr.position.can_create", "Can create position", "HR_POSITION")
    HR_POSITION_UPDATE = ("hr.position.can_update", "Can update position", "HR_POSITION")
    HR_POSITION_DELETE = ("hr.position.can_delete", "Can delete position", "HR_POSITION")
    HR_POSITION_READ = ("hr.position.can_read", "Can read position", "HR_POSITION")

    HR_ACTIVITY_CREATE = ("hr.activity.can_create", "Can create activity", "HR_ACTIVITY")
    HR_ACTIVITY_UPDATE = ("hr.activity.can_update", "Can update activity", "HR_ACTIVITY")
    HR_ACTIVITY_DELETE = ("hr.activity.can_delete", "Can delete activity", "HR_ACTIVITY")
    HR_ACTIVITY_READ = ("hr.activity.can_read", "Can read activity", "HR_ACTIVITY")
    HR_ACTIVITY_CAN_MANAGE_PARTICIPANTS = (
    "hr.activity.can_manage_participants", "Can read manage participants", "HR_ACTIVITY")

    HR_ACTIVITY_TYPE_CREATE = ("hr.activity_type.can_create", "Can create activity type", "HR_ACTIVITY_TYPE")
    HR_ACTIVITY_TYPE_UPDATE = ("hr.activity_type.can_update", "Can update activity type", "HR_ACTIVITY_TYPE")
    HR_ACTIVITY_TYPE_DELETE = ("hr.activity_type.can_delete", "Can delete activity type", "HR_ACTIVITY_TYPE")
    HR_ACTIVITY_TYPE_READ = ("hr.activity_type.can_read", "Can read activity type", "HR_ACTIVITY_TYPE")

    HR_INTERVIEW_CREATE = ("hr.interview.can_create", "Can create interview", "HR_INTERVIEW")
    HR_INTERVIEW_UPDATE = ("hr.interview.can_update", "Can update interview", "HR_INTERVIEW")
    HR_INTERVIEW_DELETE = ("hr.interview.can_delete", "Can delete interview", "HR_INTERVIEW")
    HR_INTERVIEW_READ = ("hr.interview.can_read", "Can read interview", "HR_INTERVIEW")

    HR_INTERVIEW_STEP_CREATE = ("hr.interview_step.can_create", "Can create interview step", "HR_INTERVIEW_STEP")
    HR_INTERVIEW_STEP_UPDATE = ("hr.interview_step.can_update", "Can update interview step", "HR_INTERVIEW_STEP")
    HR_INTERVIEW_STEP_DELETE = ("hr.interview_step.can_delete", "Can delete interview step", "HR_INTERVIEW_STEP")
    HR_INTERVIEW_STEP_READ = ("hr.interview_step.can_read", "Can read interview step", "HR_INTERVIEW_STEP")

    HR_VACATION_CREATE = ("hr.vacation.can_create", "Can create vacation", "HR_VACATION")
    HR_VACATION_UPDATE = ("hr.vacation.can_update", "Can update vacation", "HR_VACATION")
    HR_VACATION_DELETE = ("hr.vacation.can_delete", "Can delete vacation", "HR_VACATION")
    HR_VACATION_READ = ("hr.vacation.can_read", "Can read vacation", "HR_VACATION")
    HR_VACATION_MANAGE_FOR_OTHER = (
        "hr.vacation.can_manage_other_vacation", "Can manage other's vacation", "HR_VACATION")
    HR_VACATION_VIEW_FOR_OTHER = (
        "hr.vacation.can_view_all_vacation", "Can view other's vacation", "HR_VACATION")

    HR_CONTRACT_CREATE = ("hr.contract.can_create", "Can create contract", "HR_CONTRACT")
    HR_CONTRACT_UPDATE = ("hr.contract.can_update", "Can update contract", "HR_CONTRACT")
    HR_CONTRACT_DELETE = ("hr.contract.can_delete", "Can delete contract", "HR_CONTRACT")
    HR_CONTRACT_READ = ("hr.contract.can_read", "Can read contract", "HR_CONTRACT")
    HR_CONTRACT_CAN_MANAGE_OTHERS_CONTRACT = (
        "hr.contract.can_manage_others_contract", "Can manage other contract", "HR_CONTRACT")
    
    HR_QUESTION_CATEGORY_CREATE = ("hr.question_category.can_create", "Can create question category", "HR_QUESTION_CATEGORY",)
    HR_QUESTION_CATEGORY_UPDATE = ("hr.question_category.can_update", "Can update question category", "HR_QUESTION_CATEGORY",)
    HR_QUESTION_CATEGORY_DELETE = ("hr.question_category.can_delete", "Can delete question category", "HR_QUESTION_CATEGORY",)
    HR_QUESTION_CATEGORY_READ = ("hr.question_category.can_read", "Can read question category", "HR_QUESTION_CATEGORY")

    HR_QUESTION_CREATE = ("hr.question.can_create", "Can create question", "HR_QUESTION",)
    HR_QUESTION_UPDATE = ("hr.question.can_update", "Can update question", "HR_QUESTION",)
    HR_QUESTION_DELETE = ("hr.question.can_delete", "Can delete question", "HR_QUESTION",)
    HR_QUESTION_READ = ("hr.question.can_read", "Can read question", "HR_QUESTION")

    HR_CANDIDAT_CREATE = ("hr.candidate.can_create", "Can create candidate", "HR_CANDIDAT",)
    HR_CANDIDAT_UPDATE = ("hr.candidate.can_update", "Can update candidate", "HR_CANDIDAT",)
    HR_CANDIDAT_DELETE = ("hr.candidate.can_delete", "Can delete candidate", "HR_CANDIDAT",)
    HR_CANDIDAT_READ = ("hr.candidate.can_read", "Can read candidate", "HR_CANDIDAT",)
    HR_CANDIDAT_ADD_DOCUMENT = ("hr.candidate.can_add_document", "Can add document to candidate", "HR_CANDIDAT",)
    HR_CANDIDAT_ADD_ADDRESS = ("hr.candidate.can_add_address", "Can add address to candidate", "HR_CANDIDAT",)
    HR_CANDIDAT_ADD_CONTACT = ("hr.candidate.can_add_contact", "Can add contact to candidate", "HR_CANDIDAT",)
    HR_CANDIDAT_MANAGE_SKILL = ("hr.candidate.can_manage_skill", "Can manage candidate skills", "HR_CANDIDAT",)
    HR_CANDIDAT_MANAGE_EXPERIENCE = (
        "hr.candidate.can_manage_experience", "Can manage candidate experience", "HR_CANDIDAT",)
    
    HR_VACANCIE_CREATE = ("hr.vacancie.can_create", "Can create vacancie", "HR_VACANCIE",)
    HR_VACANCIE_UPDATE = ("hr.vacancie.can_update", "Can update vacancie", "HR_VACANCIE",)
    HR_VACANCIE_DELETE = ("hr.vacancie.can_delete", "Can delete vacancie", "HR_VACANCIE",)
    HR_VACANCIE_READ = ("hr.vacancie.can_read", "Can read vacancie", "HR_VACANCIE",)

    HR_INTERVIEW_QUESTION_CREATE = ("hr.interview_question.can_create", "Can create interview_question", "HR_INTERVIEW_QUESTION",)
    HR_INTERVIEW_QUESTION_UPDATE = ("hr.interview_question.can_update", "Can update interview_question", "HR_INTERVIEW_QUESTION",)
    HR_INTERVIEW_QUESTION_DELETE = ("hr.interview_question.can_delete", "Can delete interview_question", "HR_INTERVIEW_QUESTION",)
    HR_INTERVIEW_QUESTION_READ = ("hr.interview_question.can_read", "Can read interview_question", "HR_INTERVIEW_QUESTION",)

