from core.abstract.serializers import AbstractSerializer
from .models import BimaHrApplicantPost


class BimaHrApplicantPostSerializer(AbstractSerializer):
    class Meta:
        model = BimaHrApplicantPost
        fields = ['expected_salary', 'proposed_salary', 'accepted_salary', 'date', 'applicant', 'post']
