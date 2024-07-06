from django.core.exceptions import ValidationError


class EmailRequiredValidation(ValidationError):
    default_detail = "Email is required"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        super().__init__(detail, code)
