from django.core.exceptions import ValidationError


class UserExistsValidation(ValidationError):
    default_detail = "This email is already used"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        super().__init__(detail, code)
