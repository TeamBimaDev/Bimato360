<<<<<<< HEAD
from common.enums.interview import get_interview_status_choices, get_interview_due_data_choices,  get_interview_time_choices
from core.abstract.models import AbstractModel
from django.db import models
from hr.candidat.models import BimaHrCandidat
from hr.vacancie.models import BimaHrVacancie
from hr.interview_step.models import BimaHrInterviewStep


class BimaHrInterview(AbstractModel):
    name = models.CharField(max_length=256, blank=True, null=True)
    due_date = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_due_data_choices()) 
    scheduled_date = models.DateField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True) 
    status = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_status_choices())  
    candidat = models.ForeignKey('BimaHrCandidat', on_delete=models.CASCADE, default=1)
    vacancie = models.ForeignKey('BimaHrVacancie', on_delete=models.CASCADE, default=1)
    link_interview = models.URLField(max_length=200, blank=True, null=True)
    estimated_time = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_time_choices())
    interview_step = models.ForeignKey(BimaHrInterviewStep, null=True, blank=True, on_delete=models.PROTECT)


    def save(self, *args, **kwargs):
        if self.candidat and self.vacancie:
            self.link_interview = self.generate_link()
        super(BimaHrInterview, self).save(*args, **kwargs)

    def generate_link(self):
        # Générer un lien basé sur le nom du candidat et le nom de la vacance
        base_url = "https://interview.example.com/"
        vacancie_name = self.vacancie.title.replace(" ", "-").lower()
        candidate_name = self.candidat.first_name.replace(" ", "-").lower()
        return f"{base_url}{vacancie_name}/{candidate_name}"

    def __str__(self):
        return f"{self.name, self.vacancie.title, self.candidat.first_name}"

   

    class Meta:
        ordering = ['-name']
        permissions = []
=======
from common.enums.interview import get_interview_status_choices, get_interview_due_data_choices,  get_interview_time_choices
from core.abstract.models import AbstractModel
from django.db import models
from hr.candidat.models import BimaHrCandidat
from hr.vacancie.models import BimaHrVacancie
from hr.interview_step.models import BimaHrInterviewStep


class BimaHrInterview(AbstractModel):
    name = models.CharField(max_length=256, blank=True, null=True)
    due_date = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_due_data_choices()) 
    scheduled_date = models.DateField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True) 
    status = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_status_choices())  
    candidat = models.ForeignKey('BimaHrCandidat', on_delete=models.CASCADE, default=1)
    vacancie = models.ForeignKey('BimaHrVacancie', on_delete=models.CASCADE, default=1)
    link_interview = models.URLField(max_length=200, blank=True, null=True)
    estimated_time = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_time_choices())
    interview_step = models.ForeignKey(BimaHrInterviewStep, null=True, blank=True, on_delete=models.PROTECT)
    comments = models.TextField(blank=True)



    def save(self, *args, **kwargs):
        if self.candidat and self.vacancie:
            self.link_interview = self.generate_link()
        super(BimaHrInterview, self).save(*args, **kwargs)

    def generate_link(self):
        base_url = "https://interview.example.com/"
        vacancie_name = self.vacancie.title.replace(" ", "-").lower()
        candidate_name = self.candidat.first_name.replace(" ", "-").lower()
        return f"{base_url}{vacancie_name}/{candidate_name}"

    def __str__(self):
        return f"{self.name, self.vacancie.title, self.candidat.first_name}"

   

    class Meta:
        ordering = ['-name']
        permissions = []
>>>>>>> origin/ma-branch
