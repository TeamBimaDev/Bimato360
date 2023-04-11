from django.db import models
from core.abstract.models import AbstractModel
from hr.step.models import BimaHrInterviewStep
class BimaHrApplicant(AbstractModel):
    first_name = models.CharField(max_length=28, blank=False)
    last_name = models.CharField(max_length=28, blank=False)
    middle_name =models.CharField(max_length=28, blank=False)

    GENDER_MALE ='MALE'
    GENDER_FEMALE ='FEMALE'
    GENDER_OTHER ='OTHER'

    GENDER_CHOICES = [
        (GENDER_MALE, 'MALE'),
        (GENDER_FEMALE, 'FEMALE '),
        (GENDER_OTHER, 'OTHER'),
    ]
    gender = models.CharField(max_length=36, choices=GENDER_CHOICES)

    SOCIAL_STATUS_SINGLE ='SINGLE'
    SOCIAL_STATUS_MARRIED = 'MARRIED'
    SOCIAL_STATUS_DIVORCED ='DIVORCED'
    SOCIAL_STATUS_WIDOWED = 'WIDOWED'

    SOCIAL_STATUS_CHOICES = [
        (SOCIAL_STATUS_SINGLE, 'SINGLE'),
        (SOCIAL_STATUS_MARRIED, 'MARRIED'),
        (SOCIAL_STATUS_DIVORCED, 'DIVORCED'),
        (SOCIAL_STATUS_WIDOWED, 'WIDOWED'),
    ]
    social_status = models.CharField(max_length=36, choices=SOCIAL_STATUS_CHOICES)
    kids_number = models.IntegerField()
    social_security_number =models.CharField(max_length=255, blank=False)
    id_document_number = models.CharField(max_length=255, blank=False)
    birth_date = models.DateField()
    birth_state =models.CharField(max_length=255, blank=False)
    birth_country = models.IntegerField()
    priority =models.SmallIntegerField()
    availability_days = models.IntegerField()
    description =models.TextField(max_length=256)
    status = models.SmallIntegerField()
    refuse = models.CharField(max_length=28, blank=False)
    documents =models.IntegerField()
    id_source_type =models.IntegerField()
    Source_name =models.TextField(max_length=256)
    Score =models.FloatField()
    comments =models.TextField(max_length=256)
    steps = models.ForeignKey(BimaHrInterviewStep, on_delete=models.CASCADE)



    def __str__(self):
        return str(self.public_id)


    class Meta:
        ordering = ['first_name']
        permissions = []