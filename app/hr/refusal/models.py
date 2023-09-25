from core.abstract.models import AbstractModel
from django.db import models


class BimaHrApplicantRefusal(AbstractModel):
    who_refused = models.ForeignKey('BimaHrEmployee', on_delete=models.SET_NULL, null=True)
    when_refused = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    additional_comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.who_refused.get_full_name} on {self.when_refused}"
